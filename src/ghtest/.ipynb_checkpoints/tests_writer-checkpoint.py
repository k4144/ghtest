#!/usr/bin/env python
# coding: utf-8

from __future__ import annotations

import os
import pprint
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .tests_creator import SuggestedFunctionTests
from .test_utils import TestCaseResult, TestRunWithCassette


@dataclass
class TestArtifact:
    suggestion: SuggestedFunctionTests
    run: TestRunWithCassette


class _DataStore:
    def __init__(self, base_dir: Path, inline_limit: int = 160) -> None:
        self.base_dir = base_dir
        self.inline_limit = inline_limit
        self.counter = 0
        self.used = False
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def literal(self, value: Any, *, label: str) -> str:
        literal = _format_literal(value)
        if self._should_inline(literal):
            return literal
        filename = self._write_data_file(literal, label=label)
        return f"_load_data({filename!r})"

    def _should_inline(self, literal: str) -> bool:
        if literal is None:
            return True
        return len(literal) <= self.inline_limit

    def _write_data_file(self, literal: str, label: str) -> str:
        self.used = True
        filename = f"{label}_{self.counter}.py"
        self.counter += 1
        path = self.base_dir / filename
        path.write_text(f"DATA = {literal}\n", encoding="utf-8")
        return filename


def write_test_modules(
    artifacts: Sequence[TestArtifact],
    output_dir: str,
    *,
    max_cases_per_module: int = 10,
    inline_char_limit: int = 160,
) -> List[Path]:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    data_dir = out_dir / "data"
    data_store = _DataStore(data_dir, inline_limit=inline_char_limit)

    case_defs = _collect_cases(artifacts)
    if not case_defs:
        return []

    modules: List[Path] = []
    module_index = 0
    current_cases: List[str] = []
    needs_loader_flags: List[bool] = []

    for case_idx, case_def in enumerate(case_defs):
        test_src = _render_test_function(case_def, data_store)
        if not test_src:
            continue
        current_cases.append(test_src)
        if len(current_cases) >= max_cases_per_module:
            module_path = _write_module(
                out_dir,
                module_index,
                current_cases,
                data_loader=data_store.used,
            )
            modules.append(module_path)
            needs_loader_flags.append(data_store.used)
            current_cases = []
            module_index += 1
            data_store.used = False

    if current_cases:
        module_path = _write_module(
            out_dir,
            module_index,
            current_cases,
            data_loader=data_store.used,
        )
        modules.append(module_path)
        needs_loader_flags.append(data_store.used)

    if not any(needs_loader_flags):
        _cleanup_empty_data_dir(data_dir)

    return modules


def _cleanup_empty_data_dir(data_dir: Path) -> None:
    if not data_dir.exists():
        return
    try:
        if not any(data_dir.iterdir()):
            data_dir.rmdir()
    except OSError:
        pass


def _collect_cases(artifacts: Sequence[TestArtifact]) -> List[Tuple[SuggestedFunctionTests, TestCaseResult, int]]:
    collected: List[Tuple[SuggestedFunctionTests, TestCaseResult, int]] = []
    for artifact in artifacts:
        suggestion = artifact.suggestion
        cases = [
            case
            for case in artifact.run.cases
            if case.target == suggestion.qualname
        ]
        for idx, case in enumerate(cases):
            collected.append((suggestion, case, idx))
    return collected


def _render_test_function(
    item: Tuple[SuggestedFunctionTests, TestCaseResult, int],
    data_store: _DataStore,
) -> str:
    suggestion, case, case_idx = item
    func_name = _make_test_name(suggestion.qualname, case_idx)
    lines: List[str] = []
    lines.append(f"def {func_name}():")
    lines.append(f"    func = import_function({suggestion.module!r}, {suggestion.filepath!r}, {suggestion.qualname!r})")
    params_literal = _format_literal(case.params)
    lines.append(_format_assignment("params", params_literal))
    lines.append("    result = call_with_capture(func, target={qual!r}, params=params)".format(qual=suggestion.qualname))

    if case.exception is None:
        lines.append("    assert result.exception is None")
        return_literal = data_store.literal(case.return_value, label=f"{func_name}_return")
        lines.append(_format_assignment("expected_return", return_literal))
        lines.append("    assert result.return_value == expected_return")
    else:
        exc_type = f"{case.exception.__class__.__module__}.{case.exception.__class__.__name__}"
        message = str(case.exception)
        lines.append("    assert result.exception is not None")
        lines.append(f"    assert result.exception.__class__.__module__ + '.' + result.exception.__class__.__name__ == {exc_type!r}")
        lines.append(f"    assert str(result.exception) == {message!r}")

    printed_literal = data_store.literal(case.printed, label=f"{func_name}_stdout")
    lines.append(_format_assignment("expected_output", printed_literal))
    lines.append("    assert result.printed == expected_output")
    return "\n".join(lines) + "\n"


def _write_module(
    output_dir: Path,
    module_index: int,
    tests: List[str],
    *,
    data_loader: bool,
) -> Path:
    module_name = f"test_generated_{module_index}"
    module_path = output_dir / f"{module_name}.py"
    header_lines = ["from ghtest.test_utils import call_with_capture, import_function"]
    header = "\n".join(header_lines).rstrip() + "\n\n"
    if data_loader:
        header += "\n".join(_DATA_LOADER_TEMPLATE).rstrip() + "\n\n"
    body = "\n\n".join(tests).rstrip() + "\n"
    content = header + body
    module_path.write_text(content, encoding="utf-8")
    return module_path


def _make_test_name(qualname: str, idx: int) -> str:
    base = "".join(ch if ch.isalnum() else "_" for ch in qualname)
    base = base.strip("_") or "func"
    return f"test_{base}_case_{idx}"


def _format_literal(value: Any) -> str:
    try:
        return pprint.pformat(value, width=80, sort_dicts=True)
    except Exception:
        return repr(value)


def _format_assignment(name: str, literal: str) -> str:
    if "\n" not in literal:
        return f"    {name} = {literal}"
    lines = literal.splitlines()
    formatted = [f"    {name} = {lines[0]}"]
    formatted.extend(f"    {line}" for line in lines[1:])
    return "\n".join(formatted)


_DATA_LOADER_TEMPLATE = [
    "import importlib.util",
    "from pathlib import Path",
    "",
    "def _load_data(filename: str):",
    "    data_path = Path(__file__).with_name('data') / filename",
    "    spec = importlib.util.spec_from_file_location(f'{__name__}.{filename}', data_path)",
    "    module = importlib.util.module_from_spec(spec)",
    "    assert spec.loader is not None",
    "    spec.loader.exec_module(module)",
    "    return module.DATA",
    "",
]


__all__ = ["TestArtifact", "write_test_modules"]
