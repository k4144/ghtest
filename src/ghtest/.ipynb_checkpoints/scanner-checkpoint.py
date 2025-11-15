#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ast
import os
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


# In[2]:


@dataclass
class ParameterInfo:
    name: str
    kind: str          # "positional_only", "positional_or_keyword", "var_positional", "keyword_only", "var_keyword"
    annotation: Optional[str]
    default: Optional[str]


@dataclass
class FunctionInfo:
    module: str               # e.g. "pkg.sub.module"
    qualname: str             # e.g. "func", "Class.method", "Class.Inner.method"
    filepath: str             # path to the .py file
    lineno: int               # line number in source
    parameters: List[ParameterInfo]
    returns: Optional[str]    # return annotation as string, if any
    docstring: Optional[str]
    module_globals: Dict[str, Any] = field(default_factory=dict)

    def import_object(self) -> Callable[..., Any]:
        """
        Import and return the actual function object using module + qualname.
        """
        import importlib

        mod = importlib.import_module(self.module)
        obj: Any = mod
        for part in self.qualname.split("."):
            obj = getattr(obj, part)
        return obj


def _annotation_to_str(node: Optional[ast.expr]) -> Optional[str]:
    if node is None:
        return None
    # Use ast.unparse when available (Python 3.9+); fall back to ast.dump.
    unparse = getattr(ast, "unparse", None)
    if unparse is not None:
        try:
            return unparse(node)
        except Exception:
            pass
    return ast.dump(node)


def _expr_to_str(node: Optional[ast.expr]) -> Optional[str]:
    if node is None:
        return None
    unparse = getattr(ast, "unparse", None)
    if unparse is not None:
        try:
            return unparse(node)
        except Exception:
            pass
    return ast.dump(node)


def _extract_module_globals(tree: ast.Module) -> Dict[str, Any]:
    """
    Collect module-level assignments that look like constants, i.e. the section
    between the last import and the first function/class definition.
    """
    body = tree.body
    last_import_idx = -1
    first_def_idx = len(body)

    for idx, node in enumerate(body):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            last_import_idx = idx
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and first_def_idx == len(body):
            first_def_idx = idx

    start = last_import_idx + 1
    end = first_def_idx

    globals_dict: Dict[str, Any] = {}

    for node in body[start:end]:
        if isinstance(node, ast.Assign):
            targets = node.targets
            value_node = node.value
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
            value_node = node.value
        else:
            continue

        if value_node is None:
            continue

        try:
            value = ast.literal_eval(value_node)
        except Exception:
            continue

        for target in targets:
            if isinstance(target, ast.Name):
                globals_dict[target.id] = value

    return globals_dict


def _collect_parameters(args: ast.arguments) -> List[ParameterInfo]:
    params: List[ParameterInfo] = []

    # Positional-only args (Python 3.8+)
    posonly = getattr(args, "posonlyargs", [])
    for i, arg in enumerate(posonly):
        default_node = None
        if args.defaults:
            # defaults apply to last N positional args (posonly + normal)
            total_pos = len(posonly) + len(args.args)
            offset = total_pos - len(args.defaults)
            idx = i
            if idx >= offset:
                default_node = args.defaults[idx - offset]
        params.append(
            ParameterInfo(
                name=arg.arg,
                kind="positional_only",
                annotation=_annotation_to_str(arg.annotation),
                default=_expr_to_str(default_node),
            )
        )

    # Regular positional-or-keyword args
    total_pos = len(posonly) + len(args.args)
    for i, arg in enumerate(args.args):
        default_node = None
        if args.defaults:
            offset = total_pos - len(args.defaults)
            idx = len(posonly) + i
            if idx >= offset:
                default_node = args.defaults[idx - offset]
        params.append(
            ParameterInfo(
                name=arg.arg,
                kind="positional_or_keyword",
                annotation=_annotation_to_str(arg.annotation),
                default=_expr_to_str(default_node),
            )
        )

    # *args
    if args.vararg is not None:
        params.append(
            ParameterInfo(
                name=args.vararg.arg,
                kind="var_positional",
                annotation=_annotation_to_str(args.vararg.annotation),
                default=None,
            )
        )

    # keyword-only args
    for arg, default_node in zip(args.kwonlyargs, args.kw_defaults):
        params.append(
            ParameterInfo(
                name=arg.arg,
                kind="keyword_only",
                annotation=_annotation_to_str(arg.annotation),
                default=_expr_to_str(default_node),
            )
        )

    # **kwargs
    if args.kwarg is not None:
        params.append(
            ParameterInfo(
                name=args.kwarg.arg,
                kind="var_keyword",
                annotation=_annotation_to_str(args.kwarg.annotation),
                default=None,
            )
        )

    return params


def _module_name_from_path(root: str, filepath: str) -> str:
    rel = os.path.relpath(filepath, root)
    rel_no_ext = os.path.splitext(rel)[0]
    parts = rel_no_ext.split(os.sep)
    module = ".".join(parts)
    if module.endswith(".__init__"):
        module = module[: -len(".__init__")]
    return module or "__main__"


def scan_python_functions(root: str) -> List[FunctionInfo]:
    """
    Recursively scan a folder for Python functions (including methods in classes).

    Returns a list of FunctionInfo objects with module name, qualified name,
    source file path, parameters, return annotation, and docstring.
    """
    results: List[FunctionInfo] = []

    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if not filename.endswith(".py"):
                continue

            filepath = os.path.join(dirpath, filename)

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    source = f.read()
            except (OSError, UnicodeDecodeError):
                continue

            try:
                tree = ast.parse(source, filename=filepath)
            except SyntaxError:
                # In normal circumstances, if importing works under this Python
                # version, ast.parse should also work; this guards against
                # mismatched versions, partial files, or similar issues.
                continue

            module_name = _module_name_from_path(root, filepath)
            module_globals = _extract_module_globals(tree)

            class QualnameVisitor(ast.NodeVisitor):
                def __init__(self) -> None:
                    self.class_stack: List[str] = []

                def visit_ClassDef(self, node: ast.ClassDef) -> None:
                    self.class_stack.append(node.name)
                    self.generic_visit(node)
                    self.class_stack.pop()

                def _handle_function(self, node: ast.AST) -> None:
                    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        return

                    if self.class_stack:
                        qualname = ".".join(self.class_stack + [node.name])
                    else:
                        qualname = node.name

                    func_def = node  # type: ignore[assignment]
                    params = _collect_parameters(func_def.args)  # type: ignore[arg-type]
                    returns = _annotation_to_str(func_def.returns)  # type: ignore[arg-type]
                    docstring = ast.get_docstring(node)

                    results.append(
                        FunctionInfo(
                            module=module_name,
                            qualname=qualname,
                            filepath=filepath,
                            lineno=node.lineno,
                            parameters=params,
                            returns=returns,
                            docstring=docstring,
                            module_globals=module_globals,
                        )
                    )

                def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
                    self._handle_function(node)
                    self.generic_visit(node)

                def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
                    self._handle_function(node)
                    self.generic_visit(node)

            QualnameVisitor().visit(tree)

    return results


# In[ ]:





# In[ ]:



