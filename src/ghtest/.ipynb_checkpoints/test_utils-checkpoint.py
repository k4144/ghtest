#!/usr/bin/env python
# coding: utf-8

from __future__ import annotations

import importlib
import io
import os
import sys
import uuid
from contextlib import redirect_stdout
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


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


def _import_module_from_path(path: str, module_name: Optional[str] = None):
    if module_name is None:
        base = os.path.splitext(os.path.basename(path))[0]
        module_name = f"{base}_{uuid.uuid4().hex}"

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import module from {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def import_function(module: str, filepath: Optional[str], qualname: str) -> Callable[..., Any]:
    try:
        mod = importlib.import_module(module)
    except Exception:
        if not filepath:
            raise
        mod = _import_module_from_path(filepath)

    obj: Any = mod
    for part in qualname.split("."):
        obj = getattr(obj, part)
    return obj


def call_with_capture(
    func: Callable[..., Any],
    *,
    target: str,
    params: Dict[str, Any],
) -> TestCaseResult:
    buf = io.StringIO()
    with redirect_stdout(buf):
        try:
            ret = func(**params)
            exc: Optional[BaseException] = None
        except BaseException as error:  # noqa: BLE001
            ret = None
            exc = error
    return TestCaseResult(
        target=target,
        params=params,
        return_value=ret,
        printed=buf.getvalue(),
        exception=exc,
    )


def execute_function(
    module: str,
    filepath: Optional[str],
    qualname: str,
    params: Dict[str, Any],
) -> TestCaseResult:
    func = import_function(module, filepath, qualname)
    return call_with_capture(func, target=qualname, params=params)


__all__ = [
    "TestCaseResult",
    "TestRunWithCassette",
    "call_with_capture",
    "execute_function",
    "import_function",
]
