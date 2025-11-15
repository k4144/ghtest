#!/usr/bin/env python
# coding: utf-8

# In[2]:


import ast
import os
import sys
import importlib
import io
import textwrap
from contextlib import redirect_stdout
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


import vcr


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
class TestCaseResult:
    target: str
    params: Dict[str, Any]
    return_value: Any
    printed: str
    exception: Optional[BaseException]

@dataclass
class TestRunWithCassette:
    cassette_path: str
    cases: List[TestCaseResult]

@dataclass
class GeneratedTest:
    test_callable: Callable[[], TestRunWithCassette]
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


def _execute_function_call(module: str, filepath: str, qualname: str, params: Dict[str, Any]) -> Any:
    func = _import_function(module, filepath, qualname)
    return func(**params)


def _execute_scenario_step(step: ScenarioStep, record: bool = True) -> TestCaseResult:
    buf = io.StringIO()
    with redirect_stdout(buf):
        try:
            ret = _execute_function_call(step.module, step.filepath, step.qualname, dict(step.params))
            exc: Optional[BaseException] = None
        except BaseException as e:  # noqa: BLE001
            ret = None
            exc = e
    printed = buf.getvalue()
    if step.expect == "truthy" and not ret and exc is None:
        raise AssertionError(f"Expected truthy result for {step.qualname}, got {ret!r}")
    if step.expect == "falsy" and ret and exc is None:
        raise AssertionError(f"Expected falsy result for {step.qualname}, got {ret!r}")
    return TestCaseResult(
        target=step.qualname,
        params=step.params,
        return_value=ret,
        printed=printed,
        exception=exc,
    )


def _run_crud_scenario(scenario: CrudScenario) -> List[TestCaseResult]:
    _confirm_crud_scenario(scenario)
    results: List[TestCaseResult] = []
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


def _import_module_from_path(path: str, module_name: str = None) -> 'ModuleType':
    """
    Import a Python module directly from its file path.
    Returns the loaded module object.
    """
    if module_name is None:
        # Generate a unique name from the filename
        import os, uuid
        base = os.path.splitext(os.path.basename(path))[0]
        module_name = f"{base}_{uuid.uuid4().hex}"

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import module from {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def _import_function(module: str, filepath: str, qualname: str) -> Callable[..., Any]:
    try:
        mod = importlib.import_module(module)
    except Exception as e:
        mod=_import_module_from_path(filepath)
    obj: Any = mod
    for part in qualname.split("."):
        obj = getattr(obj, part)    
    return obj


# In[ ]:


def make_test_function(
    suggestion: SuggestedFunctionTests,
    cassette_dir: str,
    record_mode: str = "once",
) -> GeneratedTest:
    os.makedirs(cassette_dir, exist_ok=True)

    func_name = f"test_{suggestion.qualname.replace('.', '_')}"
    cassette_name = f"{suggestion.module}.{suggestion.qualname}.yaml".replace(":", "_")
    cassette_path = os.path.join(cassette_dir, cassette_name)

    vcr_recorder = vcr.VCR(
        serializer="yaml",
        cassette_library_dir=cassette_dir,
        record_mode=record_mode,
        match_on=["uri", "method"],
    )

    def test() -> TestRunWithCassette:
        if _should_confirm_execution(suggestion):
            _prompt_user_confirmation(suggestion)
        func = _import_function(suggestion.module, suggestion.filepath, suggestion.qualname)
        results: List[TestCaseResult] = []

        with vcr_recorder.use_cassette(cassette_name):
            for params in suggestion.param_sets:
                buf = io.StringIO()
                with redirect_stdout(buf):
                    try:
                        ret = func(**params)
                        exc: Optional[BaseException] = None
                    except BaseException as e:
                        ret = None
                        exc = e
                results.append(
                    TestCaseResult(
                        target=suggestion.qualname,
                        params=params,
                        return_value=ret,
                        printed=buf.getvalue(),
                        exception=exc,
                    )
                )
            if suggestion.scenario:
                scenario_results = _run_crud_scenario(suggestion.scenario)
                results.extend(scenario_results)

        return TestRunWithCassette(cassette_path=cassette_path, cases=results)

    test.__name__ = func_name
    if suggestion.docstring:
        test.__doc__ = f"Auto-generated test for {suggestion.qualname} with VCR.\n\n{suggestion.docstring}"

    param_sets_repr = repr(suggestion.param_sets)

    source = textwrap.dedent(
        f'''import importlib
import io
import os
from contextlib import redirect_stdout
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Callable

import vcr


@dataclass
class TestCaseResult:
    target: str
    params: Dict[str, Any]
    return_value: Any
    printed: str
    exception: Optional[BaseException]


@dataclass
class TestRunWithCassette:
    cassette_path: str
    cases: List[TestCaseResult]


def _import_module_from_path(path: str, module_name: str = None) -> 'ModuleType':
    """
    Import a Python module directly from its file path.
    Returns the loaded module object.
    """
    if module_name is None:
        # Generate a unique name from the filename
        import os, uuid
        base = os.path.splitext(os.path.basename(path))[0]
        module_name = f"{{base}}_{{uuid.uuid4().hex}}"

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import module from {{path}}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

    
def _import_function(module: str, filepath: str, qualname: str) -> Callable[..., Any]:
    try:
        mod = importlib.import_module(module)
    except Exception as e:
        mod=_import_module_from_path(filepath)
    obj: Any = mod
    for part in qualname.split("."):
        obj = getattr(obj, part)    
    return obj


def {func_name}() -> TestRunWithCassette:
    module = {suggestion.module!r}
    filepath = {suggestion.filepath!r}
    qualname = {suggestion.qualname!r}
    cassette_dir = {cassette_dir!r}
    cassette_name = {cassette_name!r}
    cassette_path = os.path.join(cassette_dir, cassette_name)
    param_sets = {param_sets_repr}

    os.makedirs(cassette_dir, exist_ok=True)

    vcr_recorder = vcr.VCR(
        serializer="yaml",
        cassette_library_dir=cassette_dir,
        record_mode={record_mode!r},
        match_on=["uri", "method"],
    )

    func = _import_function(module, filepath, qualname)
    results: List[TestCaseResult] = []

    with vcr_recorder.use_cassette(cassette_name):
        for params in param_sets:
            buf = io.StringIO()
            with redirect_stdout(buf):
                try:
                    ret = func(**params)
                    exc: Optional[BaseException] = None
                except BaseException as e:
                    ret = None
                    exc = e
            results.append(
                TestCaseResult(
                    target=qualname,
                    params=params,
                    return_value=ret,
                    printed=buf.getvalue(),
                    exception=exc,
                )
            )

    return TestRunWithCassette(cassette_path=cassette_path, cases=results)
        '''
    )

    return GeneratedTest(
        test_callable=test,
        cassette_path=cassette_path,
        source=source,
    )


# In[ ]:
