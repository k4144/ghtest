#!/usr/bin/env python
# coding: utf-8

# In[2]:


import ast
import os
import sys
import textwrap
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Sequence

import vcr

try:  # pragma: no cover - fallback for direct script usage
    from .test_utils import (
        CaseTestResult,
        RunTestWithCassette,
        call_with_capture,
        execute_function,
        import_function,
    )
except ImportError:  # pragma: no cover
    current_dir = os.path.dirname(__file__)
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    from test_utils import (  # type: ignore
        CaseTestResult,
        RunTestWithCassette,
        call_with_capture,
        execute_function,
        import_function,
    )


# In[5]:


@dataclass
class ScenarioStep:
    module: str
    filepath: str
    qualname: str
    params: Dict[str, Any]
    expect: Optional[str] = None
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
    module: str
    filepath: str
    qualname: str
    docstring: Optional[str]
    param_sets: List[Dict[str, Any]]   # each dict is kwargs for a call
    scenario: Optional[CrudScenario] = None


@dataclass
class GeneratedTest:
    test_callable: Callable[[], RunTestWithCassette]
    cassette_path: str
    source: str        # Python source code of an equivalent test function


_DESTRUCTIVE_NAME_HINTS = (
    "remove",
    "delete",
    "destroy",
    "drop",
    "del_",
    "rm_",
    "rmdir",
)

_DESTRUCTIVE_ATTR_HINTS = {
    ("os", "remove"),
    ("os", "rmdir"),
    ("os", "unlink"),
    ("shutil", "rmtree"),
}

_DESTRUCTIVE_SIMPLE_CALLS = {
    "remove",
    "unlink",
    "rmdir",
    "rmtree",
    "delete",
    "del",
    "rmtree",
}


def _looks_destructive_name(qualname: str) -> bool:
    lname = qualname.lower()
    return any(token in lname for token in _DESTRUCTIVE_NAME_HINTS)


def _load_function_ast(filepath: str) -> Optional[ast.Module]:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except OSError:
        return None

    try:
        return ast.parse(source, filename=filepath)
    except SyntaxError:
        return None


class _FunctionFinder(ast.NodeVisitor):
    def __init__(self, target: str) -> None:
        self.target = target
        self.stack: List[str] = []
        self.found: Optional[ast.AST] = None

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        if self.found:
            return
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if self.found:
            return
        current = ".".join(self.stack + [node.name])
        if current == self.target:
            self.found = node
            return
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.visit_FunctionDef(node)  # type: ignore[arg-type]


class _DestructiveCallVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.found = False

    def visit_Call(self, node: ast.Call) -> None:
        if self.found:
            return
        if _is_destructive_call(node):
            self.found = True
            return
        self.generic_visit(node)


def _is_destructive_call(node: ast.Call) -> bool:
    func = node.func
    if isinstance(func, ast.Attribute):
        attr = func.attr.lower()
        base = func.value
        if isinstance(base, ast.Name):
            base_name = base.id.lower()
            if (base_name, attr) in _DESTRUCTIVE_ATTR_HINTS:
                return True
        if attr in _DESTRUCTIVE_SIMPLE_CALLS:
            return True
    elif isinstance(func, ast.Name):
        if func.id.lower() in _DESTRUCTIVE_SIMPLE_CALLS:
            return True
    return False


def _function_body_has_destructive_calls(filepath: str, qualname: str) -> bool:
    tree = _load_function_ast(filepath)
    if tree is None:
        return False
    finder = _FunctionFinder(qualname)
    finder.visit(tree)
    if finder.found is None:
        return False
    visitor = _DestructiveCallVisitor()
    visitor.visit(finder.found)  # type: ignore[arg-type]
    return visitor.found


def _should_confirm_execution(suggestion: SuggestedFunctionTests) -> bool:
    if _looks_destructive_name(suggestion.qualname):
        return True
    return _function_body_has_destructive_calls(suggestion.filepath, suggestion.qualname)


def _prompt_user_confirmation(suggestion: SuggestedFunctionTests) -> None:
    if os.environ.get("GHTEST_ASSUME_SAFE") == "1":
        return
    prompt = (
        f"Function {suggestion.qualname} in {suggestion.filepath} may perform destructive actions.\n"
        "Proceed with executing auto-generated tests? [y/N]: "
    )
    response = input(prompt)
    if response.strip().lower() not in {"y", "yes"}:
        raise RuntimeError("Aborted executing potentially destructive test target.")


def _format_step_summary(step: ScenarioStep) -> str:
    param_display = ", ".join(f"{k}={v!r}" for k, v in step.params.items())
    return f"{step.qualname}({param_display})"


def _confirm_crud_scenario(scenario: CrudScenario) -> None:
    if os.environ.get("GHTEST_ASSUME_SAFE") == "1":
        return
    lines = [
        f"Planned CRUD scenario for resource '{scenario.resource}' as '{scenario.identifier}':",
    ]
    for step in scenario.steps:
        lines.append(f"  - {_format_step_summary(step)}")
    if scenario.note:
        lines.append(f"Note: {scenario.note}")
    lines.append("Proceed with the full sequence? [y/N]: ")
    response = input("\n".join(lines))
    if response.strip().lower() not in {"y", "yes"}:
        raise RuntimeError("Aborted CRUD scenario execution.")


def _execute_scenario_step(step: ScenarioStep, record: bool = True) -> CaseTestResult:
    result = execute_function(step.module, step.filepath, step.qualname, dict(step.params))
    ret = result.return_value
    exc = result.exception
    if step.expect == "truthy" and not ret and exc is None:
        raise AssertionError(f"Expected truthy result for {step.qualname}, got {ret!r}")
    if step.expect == "falsy" and ret and exc is None:
        raise AssertionError(f"Expected falsy result for {step.qualname}, got {ret!r}")
    return result


def _run_crud_scenario(scenario: CrudScenario) -> List[CaseTestResult]:
    _confirm_crud_scenario(scenario)
    results: List[CaseTestResult] = []
    cleanup_step = next((s for s in scenario.steps if s.cleanup), None)
    cleanup_executed = False
    pending_error: Optional[BaseException] = None

    try:
        for step in scenario.steps:
            result = _execute_scenario_step(step)
            results.append(result)
            if step.cleanup and result.exception is None:
                cleanup_executed = True
            if result.exception is not None:
                raise result.exception
    except BaseException as exc:  # noqa: BLE001
        pending_error = exc
    finally:
        if cleanup_step and not cleanup_executed:
            try:
                _execute_scenario_step(cleanup_step, record=False)
            except Exception:
                pass
    if pending_error:
        raise pending_error
    return results


def make_test_function(
    suggestion: SuggestedFunctionTests,
    cassette_dir: str,
    record_mode: str = "once",
    volatile_response_fields: Optional[Sequence[str]] = None,
) -> GeneratedTest:
    os.makedirs(cassette_dir, exist_ok=True)

    func_name = f"test_{suggestion.qualname.replace('.', '_')}"
    cassette_base = f"{suggestion.module}.{suggestion.qualname}".replace(":", "_")
    cassette_path = os.path.join(cassette_dir, f"{cassette_base}.yaml")
    if volatile_response_fields is None:
        volatile_fields: Optional[List[str]] = None
    else:
        volatile_fields = list(volatile_response_fields)

    def test() -> RunTestWithCassette:
        if _should_confirm_execution(suggestion):
            _prompt_user_confirmation(suggestion)
        func = import_function(suggestion.module, suggestion.filepath, suggestion.qualname)
        results: List[CaseTestResult] = []

        for idx, params in enumerate(suggestion.param_sets):
            case_cassette = f"{cassette_base}.case_{idx}.yaml"
            recorder = vcr.VCR(
                serializer="yaml",
                cassette_library_dir=cassette_dir,
                record_mode=record_mode,
                match_on=["uri", "method", "body"],
            )
            with recorder.use_cassette(case_cassette):
                result = call_with_capture(
                    func,
                    target=suggestion.qualname,
                    params=dict(params),
                    volatile_return_fields=volatile_fields,
                )
            result.cassette_path = os.path.join(cassette_dir, case_cassette)
            results.append(result)

        if suggestion.scenario:
            scenario_results = _run_crud_scenario(suggestion.scenario)
            results.extend(scenario_results)

        return RunTestWithCassette(
            cassette_path=cassette_path,
            cases=results,
        )

    test.__name__ = func_name
    if suggestion.docstring:
        test.__doc__ = f"Auto-generated test for {suggestion.qualname} with VCR.\n\n{suggestion.docstring}"

    param_sets_repr = repr(suggestion.param_sets)
    volatile_repr = repr(volatile_fields)

    source = textwrap.dedent(
        f'''import os
from typing import List

import vcr

from ghtest.test_utils import (
    CaseTestResult,
    RunTestWithCassette,
    call_with_capture,
    import_function,
)


def {func_name}() -> RunTestWithCassette:
    module = {suggestion.module!r}
    filepath = {suggestion.filepath!r}
    qualname = {suggestion.qualname!r}
    cassette_dir = {cassette_dir!r}
    cassette_base = {cassette_base!r}
    cassette_path = os.path.join(cassette_dir, f"{{cassette_base}}.yaml")
    param_sets = {param_sets_repr}
    volatile_fields = {volatile_repr}

    os.makedirs(cassette_dir, exist_ok=True)

    func = import_function(module, filepath, qualname)
    results: List[CaseTestResult] = []

    for idx, params in enumerate(param_sets):
        recorder = vcr.VCR(
            serializer="yaml",
            cassette_library_dir=cassette_dir,
            record_mode={record_mode!r},
            match_on=["uri", "method", "body"],
        )
        cassette_name = f"{cassette_base}.case_{{idx}}.yaml"
        with recorder.use_cassette(cassette_name):
            result = call_with_capture(func, target=qualname, params=params, volatile_return_fields=volatile_fields)
        result.cassette_path = os.path.join(cassette_dir, cassette_name)
        results.append(result)

    return RunTestWithCassette(cassette_path=os.path.join(cassette_dir, f"{cassette_base}.yaml"), cases=results)
        '''
    )

    return GeneratedTest(
        test_callable=test,
        cassette_path=cassette_path,
        source=source,
    )


# In[ ]:
