#!/usr/bin/env python
# coding: utf-8

import ast
import json
import os
import random
import string
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

VERBOSITY_PARAM_TOKENS = ("verbose", "verbosity", "vb", "print", "show")
_PARAM_HISTORY_ENV = "GHTEST_PARAM_HISTORY"
_PARAM_HISTORY_CACHE: Optional[Dict[str, List[Any]]] = None
_LITERAL_ASSIGNMENTS_CACHE: Dict[str, Dict[str, List[Any]]] = {}
VB=0


@dataclass
class ScenarioStep:
    module: str
    filepath: str
    qualname: str
    params: Dict[str, Any]
    expect: Optional[str] = None  # "truthy" | "falsy" | None
    cleanup: bool = False
    description: Optional[str] = None


@dataclass
class CrudScenario:
    resource: str
    identifier: str
    steps: List[ScenarioStep]
    note: Optional[str] = None


@dataclass
class SuggestedFunctionTests:
    module: str              # import path, e.g. "pkg.sub.module"
    filepath: str
    qualname: str            # "func", "Class.method", ...
    docstring: Optional[str]
    param_sets: List[Dict[str, Any]]  # each dict is kwargs for a call
    scenario: Optional[CrudScenario] = None


def _extract_module_globals_from_file(filepath: str) -> Dict[str, Any]:
    """
    Parse the module source and extract top-level assignments that are likely
    to be constants (between the last import and the first def/class).
    """
    try:
        if VB:print(f'_extract_module_globals: reading {filepath}')
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except OSError:
        return {}

    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        return {}

    body = tree.body
    last_import_idx = -1
    first_def_idx = len(body)

    for i, node in enumerate(body):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            last_import_idx = i
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and first_def_idx == len(body):
            first_def_idx = i

    start = last_import_idx + 1
    end = first_def_idx

    globals_dict: Dict[str, Any] = {}

    for node in body[start:end]:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            value_node = node.value
            if value_node is None:
                continue
            try:
                value = ast.literal_eval(value_node)
            except Exception:
                continue

            if isinstance(node, ast.Assign):
                targets = node.targets
            else:
                targets = [node.target]

            for target in targets:
                if isinstance(target, ast.Name):
                    globals_dict[target.id] = value

    return globals_dict


def _literal_eval_assign(node: ast.AST) -> Tuple[bool, Optional[Any]]:
    try:
        return True, ast.literal_eval(node)
    except Exception:
        return False, None


def _iter_assignment_names(target: ast.AST):
    if isinstance(target, ast.Name):
        yield target.id.lower()
    elif isinstance(target, (ast.Tuple, ast.List)):
        for elt in target.elts:
            yield from _iter_assignment_names(elt)


class _LiteralAssignmentCollector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.values: Dict[str, List[Any]] = defaultdict(list)

    def _add(self, name: str, value: Any) -> None:
        bucket = self.values[name]
        if value not in bucket:
            bucket.append(value)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        # Skip function bodies to avoid picking up local assignments.
        return

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        return

    def visit_Assign(self, node: ast.Assign) -> None:
        success, value = _literal_eval_assign(node.value)
        if not success:
            return
        for target in node.targets:
            for name in _iter_assignment_names(target):
                self._add(name, value)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if node.value is None:
            return
        success, value = _literal_eval_assign(node.value)
        if not success:
            return
        target = node.target
        for name in _iter_assignment_names(target):
            self._add(name, value)


def _extract_literal_assignments_from_file(filepath: Optional[str]) -> Dict[str, List[Any]]:
    if not filepath:
        return {}
    cached = _LITERAL_ASSIGNMENTS_CACHE.get(filepath)
    if cached is not None:
        return cached
    try:
        if VB:print(f'_extract_literal: reading {filepath}')
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except OSError:
        _LITERAL_ASSIGNMENTS_CACHE[filepath] = {}
        return {}
    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        _LITERAL_ASSIGNMENTS_CACHE[filepath] = {}
        return {}

    collector = _LiteralAssignmentCollector()
    collector.visit(tree)
    result = dict(collector.values)
    _LITERAL_ASSIGNMENTS_CACHE[filepath] = result
    return result


def _strip_numeric_suffix(name: str) -> str:
    stripped = name.rstrip("0123456789")
    if stripped.endswith("_"):
        stripped = stripped.rstrip("_")
    return stripped


_ENV_PLACEHOLDER_SUFFIXES = {"term", "key", "token", "secret", "env", "var"}


def _looks_like_env_placeholder(tokens: List[str], pname: str) -> bool:
    if not tokens:
        return False
    last = tokens[-1]
    if last not in _ENV_PLACEHOLDER_SUFFIXES:
        return False
    if last in pname:
        return False
    return True


def _choose_global_for_param(
    param: "ParameterInfo",
    module_globals: Dict[str, Any],
) -> Optional[Any]:
    """
    Try to find a suitable module-level constant for this parameter, based on
    name similarity and (optionally) annotation / value type.
    """
    if not module_globals:
        return None

    pname = param.name.lower()
    ann = (param.annotation or "").lower()

    best_score = 0
    best_value: Any = None

    for gname, gval in module_globals.items():
        gname_lower = gname.lower()
        stripped = _strip_numeric_suffix(gname_lower)
        tokens = [tok for tok in stripped.split("_") if tok]
        score = 0

        if stripped == pname or gname_lower == pname:
            score = 5
        elif stripped.endswith("_" + pname):
            score = 4
        elif pname in tokens:
            score = 3
        elif stripped.endswith(pname):
            score = 2
        elif pname in gname_lower:
            score = 1

        if score == 0:
            continue

        if _looks_like_env_placeholder(tokens, pname):
            continue

        if ann:
            if "str" in ann and not isinstance(gval, str):
                continue
            if ("int" in ann or "integer" in ann) and not isinstance(gval, int):
                continue
            if "float" in ann and not isinstance(gval, float):
                continue
            if "bool" in ann and not isinstance(gval, bool):
                continue

        if score > best_score:
            best_score = score
            best_value = gval

    return best_value


def _select_preferred_hint(values: Optional[List[Any]]) -> Optional[Any]:
    if not values:
        return None
    for value in values:
        if value is not None:
            return value
    return values[0]


def _guess_example_value(
    param: "ParameterInfo",
    func: "FunctionInfo",
    module_globals: Optional[Dict[str, Any]] = None,
    module_param_values: Optional[Dict[str, List[Any]]] = None,
    literal_assignments: Optional[Dict[str, List[Any]]] = None,
    history_values: Optional[Dict[str, List[Any]]] = None,
    include_source: bool = False,
) -> Any:
    """
    Heuristic guess of a reasonable example value for a parameter,
    considering module-level constants in the function's module.
    """
    source = "heuristic"
    default_value = getattr(param, "default_value", None)
    def _finish(val: Any) -> Any:
        return (val, source) if include_source else val

    if literal_assignments:
        literal = _select_preferred_hint(literal_assignments.get(param.name.lower()))
        if literal is not None:
            if include_source:
                return literal, "literal_assignment"
            return literal

    if module_globals:
        global_match = _choose_global_for_param(param, module_globals)
        if global_match is not None:
            if include_source:
                return global_match, "module_global"
            return global_match

    if module_param_values:
        hints = _select_preferred_hint(module_param_values.get(param.name))
        if hints is not None:
            if include_source:
                return hints, "module_param"
            return hints

    if history_values:
        history = _select_preferred_hint(history_values.get(param.name.lower()))
        if history is not None:
            if include_source:
                return history, "history"
            return history

    name = param.name.lower()
    ann = (param.annotation or "").lower()
    if not ann and default_value is not None:
        ann = type(default_value).__name__.lower()
    doc = (func.docstring or "").lower()

    if ann in {"bool", "builtins.bool", "typing.bool"} or \
       name.startswith("is_") or name.startswith("has_") or name.endswith("_flag"):
        value = default_value if isinstance(default_value, bool) else True
        return _finish(value)

    if "path" in name or "file" in name or "filename" in name:
        value = "example.txt"
        return _finish(value)
    if "dir" in name or "folder" in name:
        value = "example_dir"
        return _finish(value)

    if "url" in name or "uri" in name:
        value = "https://example.com"
        return _finish(value)

    if ann in {"int", "builtins.int"} or \
       any(k in name for k in ["count", "num", "size", "length", "index"]) or \
       name in {"n", "i", "j", "k"}:
        value = default_value if isinstance(default_value, int) else 1
        return _finish(value)

    if ann in {"float", "builtins.float"} or "timeout" in name or "seconds" in name:
        value = default_value if isinstance(default_value, float) else 1.0
        return _finish(value)

    if ("list" in ann or "sequence" in ann or "tuple" in ann) or name.endswith("s"):
        value = default_value if isinstance(default_value, (list, tuple)) else [1, 2]
        return _finish(value)

    if "dict" in ann or "mapping" in ann or "map" in name:
        value = default_value if isinstance(default_value, dict) else {"key": "value"}
        return _finish(value)

    if "data" in name or "payload" in name or "json" in name:
        value = default_value if isinstance(default_value, dict) else {"data": "example"}
        return _finish(value)

    if ann in {"str", "builtins.str"} or "name" in name or "label" in name or "key" in name:
        value = default_value if isinstance(default_value, str) else "example"
        return _finish(value)

    if "path" in doc and ("file" in name or "path" in name):
        value = "example.txt"
        return _finish(value)

    value = default_value if isinstance(default_value, str) else "example"
    return _finish(value)


def _build_minimal_kwargs(
    func: "FunctionInfo",
    module_globals: Dict[str, Any],
    module_param_values: Dict[str, List[Any]],
    literal_assignments: Dict[str, List[Any]],
    history_values: Dict[str, List[Any]],
) -> Dict[str, Any]:
    required: List["ParameterInfo"] = []

    is_method = "." in func.qualname
    for idx, p in enumerate(func.parameters):
        if is_method and idx == 0 and p.name in {"self", "cls"}:
            continue
        if p.kind in {"var_positional", "var_keyword"}:
            continue
        if p.default is None:
            required.append(p)

    kwargs: Dict[str, Any] = {}
    for p in required:
        kwargs[p.name] = _guess_example_value(
            p,
            func,
            module_globals=module_globals,
            module_param_values=module_param_values,
            literal_assignments=literal_assignments,
            history_values=history_values,
        )
    return kwargs


def _apply_resource_identifier(kwargs: Dict[str, Any], func: "FunctionInfo", identifier: str) -> None:
    candidate_names = {"name", "slug", "repo", "item", "resource", "id"}
    resource_lower = (func.crud_resource or "").lower()
    for p in func.parameters:
        pname = p.name
        lower = pname.lower()
        if pname in kwargs:
            continue
        if lower in candidate_names or (resource_lower and resource_lower in lower):
            kwargs[pname] = identifier
    for key in list(kwargs.keys()):
        lower = key.lower()
        if lower in candidate_names or (resource_lower and resource_lower in lower):
            kwargs[key] = identifier


def _build_crud_scenario(
    func: "FunctionInfo",
    module_globals: Dict[str, Any],
    module_param_values: Dict[str, List[Any]],
    literal_assignments: Dict[str, List[Any]],
    history_values: Dict[str, List[Any]],
) -> Optional[CrudScenario]:
    if getattr(func, "crud_role", None) != "create":
        return None

    resource = func.crud_resource or func.qualname.split(".")[-1]
    peers = [f for f in getattr(func, "module_functions", []) if f is not func]
    delete_func = next(
        (f for f in peers if f.crud_resource == func.crud_resource and f.crud_role == "delete"),
        None,
    )
    read_func = next(
        (f for f in peers if f.crud_resource == func.crud_resource and f.crud_role in {"read", "list"}),
        None,
    )
    if not delete_func or not read_func:
        return None

    identifier = _generate_resource_identifier(resource)

    def build_kwargs(target: "FunctionInfo", overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        kwargs = _build_minimal_kwargs(
            target,
            module_globals,
            module_param_values,
            literal_assignments,
            history_values,
        )
        if overrides:
            for key, value in overrides.items():
                if any(p.name == key for p in target.parameters):
                    kwargs[key] = value
        _apply_resource_identifier(kwargs, target, identifier)
        return kwargs

    steps: List[ScenarioStep] = []

    pre_get = build_kwargs(read_func, {"dry_run": False})
    steps.append(
        ScenarioStep(
            module=read_func.module,
            filepath=read_func.filepath,
            qualname=read_func.qualname,
            params=pre_get,
            expect="falsy",
            description="Ensure resource does not exist before creation.",
        )
    )

    create_kwargs = build_kwargs(func, {"dry_run": False})
    steps.append(
        ScenarioStep(
            module=func.module,
            filepath=func.filepath,
            qualname=func.qualname,
            params=create_kwargs,
            expect="truthy",
            description="Create resource instance.",
        )
    )

    post_get = build_kwargs(read_func, {"dry_run": False})
    steps.append(
        ScenarioStep(
            module=read_func.module,
            filepath=read_func.filepath,
            qualname=read_func.qualname,
            params=post_get,
            expect="truthy",
            description="Validate resource exists after creation.",
        )
    )

    delete_kwargs = build_kwargs(delete_func, {"dry_run": False, "force": True})
    steps.append(
        ScenarioStep(
            module=delete_func.module,
            filepath=delete_func.filepath,
            qualname=delete_func.qualname,
            params=delete_kwargs,
            expect="truthy",
            cleanup=True,
            description="Delete the resource to leave no residue.",
        )
    )

    final_get = build_kwargs(read_func, {"dry_run": False})
    steps.append(
        ScenarioStep(
            module=read_func.module,
            filepath=read_func.filepath,
            qualname=read_func.qualname,
            params=final_get,
            expect="falsy",
            description="Ensure resource is gone after deletion.",
        )
    )

    note = "Set GHTEST_ASSUME_SAFE=1 to skip confirmations before running this scenario."

    return CrudScenario(
        resource=resource or "resource",
        identifier=identifier,
        steps=steps,
        note=note,
    )


def _guess_alternative_value(value: Any, *, from_module_global: bool = False) -> Any:
    """
    Given a baseline example value, produce a different one for
    tests that override defaults.
    """
    if from_module_global:
        return value
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, float):
        return value * 2 or 1.0
    if isinstance(value, str):
        return value + "_alt"
    if isinstance(value, list):
        return value + value
    if isinstance(value, dict):
        new = dict(value)
        new["extra"] = "alt"
        return new
    return (value, "alt")


def _safe_literal_eval(node: ast.AST) -> Any:
    """
    Best-effort literal_eval wrapper for arguments in test calls.
    Returns a Python value or raises if not evaluable.
    """
    return ast.literal_eval(node)


def _is_call_to_target(call: ast.Call, target_name: str) -> bool:
    fn = call.func
    if isinstance(fn, ast.Name):
        return fn.id == target_name
    if isinstance(fn, ast.Attribute):
        return fn.attr == target_name
    return False


def _extract_param_sets_from_test_function(
    func: "FunctionInfo",
    test_func: "FunctionInfo",
) -> List[Dict[str, Any]]:
    """
    From a single test function, extract argument sets for calls to the
    function under test, based on literal arguments.
    """
    target_name = func.qualname.split(".")[-1]
    test_name = test_func.qualname.split(".")[-1]
    if not test_name.startswith("test_"):
        return []

    try:
        if VB:print(f'_extract_param_sets: reading {filepath}')
        with open(test_func.filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except OSError:
        return []

    try:
        tree = ast.parse(source, filename=test_func.filepath)
    except SyntaxError:
        return []

    desired_test_def: Optional[ast.FunctionDef] = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == test_name:
            desired_test_def = node
            break

    if desired_test_def is None:
        return []

    params = func.parameters
    if not params:
        return []

    is_method = "." in func.qualname and params[0].name in {"self", "cls"}
    start_index = 1 if is_method else 0

    param_sets: List[Dict[str, Any]] = []

    sample_calls = getattr(func, "sample_calls", None) or []
    for sample in sample_calls:
        param_sets.append(dict(sample))

    for node in ast.walk(desired_test_def):
        if not isinstance(node, ast.Call):
            continue
        if not _is_call_to_target(node, target_name):
            continue

        kwargs: Dict[str, Any] = {}
        ok = True

        try:
            for i, arg_node in enumerate(node.args):
                param_index = start_index + i
                if param_index >= len(params):
                    break
                pname = params[params_index].name
                value = _safe_literal_eval(arg_node)
                kwargs[pname] = value

            for kw in node.keywords:
                if kw.arg is None:
                    continue
                value = _safe_literal_eval(kw.value)
                kwargs[kw.arg] = value
        except Exception:
            ok = False

        if ok and kwargs:
            param_sets.append(kwargs)

    return param_sets


def _extract_test_param_sets_for_func(
    func: "FunctionInfo",
    test_funcs: List["FunctionInfo"],
) -> List[Dict[str, Any]]:
    """
    Look through all test functions and collect param sets for calls to func.
    Test functions are identified by name test_{function_under_test} and
    the call must actually appear inside the test body.
    """
    if not test_funcs:
        return []

    target_name = func.qualname.split(".")[-1]
    expected_test_name = f"test_{target_name}"

    matching_tests = [
        tf
        for tf in test_funcs
        if tf.qualname.split(".")[-1] == expected_test_name
    ]

    all_param_sets: List[Dict[str, Any]] = []
    for tf in matching_tests:
        all_param_sets.extend(_extract_param_sets_from_test_function(func, tf))

    return all_param_sets


def _dedupe_param_sets(param_sets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    result: List[Dict[str, Any]] = []
    for ps in param_sets:
        key = tuple(sorted(ps.items()))
        if key in seen:
            continue
        seen.add(key)
        result.append(ps)
    return result


def suggest_params(
    func: "FunctionInfo",
    test_functions: Optional[List["FunctionInfo"]] = None,
) -> SuggestedFunctionTests:
    """
    Suggest parameter sets for tests of a single FunctionInfo.

    Uses three sources, in order of preference:
    1) Existing test functions (from a tests folder) that call the function.
    2) A minimal set using only required parameters (skipping self/cls).
    3) Additional sets where defaulted parameters are given alternative values.

    test_functions should be the scanner results from the tests directory.
    """
    required: List["ParameterInfo"] = []
    optional: List["ParameterInfo"] = []

    is_method = "." in func.qualname

    for idx, p in enumerate(func.parameters):
        if is_method and idx == 0 and p.name in {"self", "cls"}:
            continue

        if p.kind in {"var_positional", "var_keyword"}:
            continue

        is_required = p.default is None
        if is_required:
            required.append(p)
        else:
            optional.append(p)

    module_globals = getattr(func, "module_globals", None) or {}
    if not module_globals:
        filepath = getattr(func, "filepath", None)
        if isinstance(filepath, str):
            module_globals = _extract_module_globals_from_file(filepath)
    module_param_values = getattr(func, "module_param_values", None) or {}
    filepath = getattr(func, "filepath", None)
    literal_assignments = _extract_literal_assignments_from_file(filepath)
    history_values = _load_param_history()

    param_sets: List[Dict[str, Any]] = []
    observed_values: Dict[str, List[Any]] = defaultdict(list)

    def _record(call_kwargs: Dict[str, Any]) -> None:
        for name, value in call_kwargs.items():
            if not _is_serializable_value(value):
                continue
            bucket = observed_values.setdefault(name, [])
            if value not in bucket:
                bucket.append(value)

    for name, values in module_param_values.items():
        for value in values:
            if not _is_serializable_value(value):
                continue
            bucket = observed_values.setdefault(name, [])
            if value not in bucket:
                bucket.append(value)

    module_call_values = getattr(func, "module_call_values", None) or []
    for call in module_call_values:
        call_copy = dict(call)
        param_sets.append(call_copy)
        _record(call_copy)

    sample_calls = getattr(func, "sample_calls", None) or []
    for sample in sample_calls:
        sample_copy = dict(sample)
        param_sets.append(sample_copy)
        _record(sample_copy)

    if test_functions:
        test_param_sets = _extract_test_param_sets_for_func(func, test_functions)
        param_sets.extend(test_param_sets)
        for call_kwargs in test_param_sets:
            _record(call_kwargs)

    minimal: Dict[str, Any] = {}
    for p in required:
        minimal[p.name] = _guess_example_value(
            p,
            func,
            module_globals=module_globals,
            module_param_values=module_param_values,
            literal_assignments=literal_assignments,
            history_values=history_values,
        )

    param_sets.append(minimal)
    _record(minimal)

    for opt in optional:
        call_kwargs = dict(minimal)
        baseline, source = _guess_example_value(
            opt,
            func,
            module_globals=module_globals,
            module_param_values=module_param_values,
            literal_assignments=literal_assignments,
            history_values=history_values,
            include_source=True,
        )
        alt = _guess_alternative_value(
            baseline,
            from_module_global=(source == "module_global"),
        )
        call_kwargs[opt.name] = alt
        param_sets.append(call_kwargs)
        _record(call_kwargs)

    verbosity_params = required + optional
    for p in verbosity_params:
        candidate_values = _verbosity_candidate_values(p)
        if not candidate_values:
            continue
        for value in candidate_values:
            call_kwargs = dict(minimal)
            call_kwargs[p.name] = value
            param_sets.append(call_kwargs)
            _record(call_kwargs)

    param_sets = _dedupe_param_sets(param_sets)
    _update_param_history(observed_values)

    scenario = None
    if getattr(func, "crud_role", None) == "create":
        scenario = _build_crud_scenario(
            func,
            module_globals,
            module_param_values,
            literal_assignments,
            history_values,
        )

    return SuggestedFunctionTests(
        module=func.module,
        filepath=func.filepath,
        qualname=func.qualname,
        docstring=func.docstring,
        param_sets=param_sets,
        scenario=scenario,
    )
def _is_verbosity_param(name: str) -> bool:
    lname = name.lower()
    for token in VERBOSITY_PARAM_TOKENS:
        if token == "vb":
            if lname == "vb" or lname.startswith("vb_") or lname.endswith("_vb"):
                return True
        if token in lname:
            return True
    return False


def _verbosity_candidate_values(param: "ParameterInfo") -> Optional[List[Any]]:
    if not _is_verbosity_param(param.name):
        return None

    ann = (param.annotation or "").lower()
    default_value = getattr(param, "default_value", None)

    if "bool" in ann or isinstance(default_value, bool):
        base = [False, True]
    elif "int" in ann or (isinstance(default_value, int) and not isinstance(default_value, bool)):
        base = [0, 1, 2, 3]
    else:
        base = [False, True]

    if default_value is not None and default_value not in base:
        base.append(default_value)

    seen = set()
    ordered: List[Any] = []
    for value in base:
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered
def _history_path() -> Path:
    env = os.environ.get(_PARAM_HISTORY_ENV)
    if env:
        return Path(env)
    state_home = os.environ.get("XDG_STATE_HOME")
    if state_home:
        base = Path(state_home)
    else:
        base = Path.home() / ".local" / "state"
    return base / "ghtest" / "param_history.json"


def _is_serializable_value(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, (bool, int, float, str)):
        return True
    if isinstance(value, list):
        return all(_is_serializable_value(v) for v in value)
    if isinstance(value, dict):
        return all(isinstance(k, str) and _is_serializable_value(v) for k, v in value.items())
    return False


def _load_param_history() -> Dict[str, List[Any]]:
    global _PARAM_HISTORY_CACHE
    if _PARAM_HISTORY_CACHE is not None:
        return _PARAM_HISTORY_CACHE

    path = _history_path()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            _PARAM_HISTORY_CACHE = {str(k).lower(): list(v) for k, v in data.items()}
        else:
            _PARAM_HISTORY_CACHE = {}
    except FileNotFoundError:
        _PARAM_HISTORY_CACHE = {}
    except json.JSONDecodeError:
        _PARAM_HISTORY_CACHE = {}
    return _PARAM_HISTORY_CACHE


def _save_param_history(history: Dict[str, List[Any]]) -> None:
    path = _history_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")


def _history_values_for(name: str) -> List[Any]:
    history = _load_param_history()
    return history.get(name.lower(), [])


def _update_param_history(observed: Dict[str, List[Any]]) -> None:
    if not observed:
        return
    history = _load_param_history()
    changed = False
    for name, values in observed.items():
        key = name.lower()
        bucket = history.setdefault(key, [])
        for value in values:
            if not _is_serializable_value(value):
                continue
            if value not in bucket:
                bucket.append(value)
                changed = True
    if changed:
        _save_param_history(history)


def _generate_resource_identifier(resource: Optional[str]) -> str:
    prefix = "".join(ch for ch in (resource or "") if ch.isalpha()).lower() or "item"
    prefix = prefix[:3] if prefix else "itm"
    if not prefix[0].isalpha():
        prefix = "a" + prefix[1:]
    suffix = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    return f"{prefix}{suffix}"
