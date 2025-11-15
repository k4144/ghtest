import importlib.util
import os
import sys
import tempfile
import textwrap
import types
import unittest
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
PKG_DIR = SRC_DIR / "ghtest"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

try:  # pragma: no cover - optional dependency
    import vcr  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    class _StubVCR:
        def __init__(self, *_, **__):
            pass

        def use_cassette(self, *_args, **__kwargs):
            @contextmanager
            def _noop():
                yield

            return _noop()

    sys.modules["vcr"] = types.SimpleNamespace(VCR=_StubVCR)


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


tests_creator = _load_module("test_tests_creator_mod", PKG_DIR / "tests_creator.py")
param_suggestor = _load_module("test_param_suggestor_for_creator", PKG_DIR / "param_suggestor.py")
scanner = _load_module("test_scanner_for_creator", PKG_DIR / "scanner.py")

HISTORY_FILE = Path(tempfile.gettempdir()) / "ghtest_creator_history.json"
os.environ["GHTEST_PARAM_HISTORY"] = str(HISTORY_FILE)
if HISTORY_FILE.exists():
    HISTORY_FILE.unlink()


DESTRUCTIVE_MODULE = textwrap.dedent(
    """
    import shutil


    def delete_temp(path):
        shutil.rmtree(path)


    def clean_directory(path):
        shutil.rmtree(path)


    def describe(path):
        return path
    """
)


class TestsCreatorSafeguardTests(unittest.TestCase):
    def _write_module(self, tmpdir: str) -> Path:
        root = Path(tmpdir)
        pkg = root / "samplepkg"
        pkg.mkdir()
        (pkg / "__init__.py").write_text("", encoding="utf-8")
        module_path = pkg / "ops.py"
        module_path.write_text(DESTRUCTIVE_MODULE, encoding="utf-8")
        return module_path

    def _suggestion(self, filepath: Path, qualname: str) -> tests_creator.SuggestedFunctionTests:
        return tests_creator.SuggestedFunctionTests(
            module="samplepkg.ops",
            filepath=str(filepath),
            qualname=qualname,
            docstring=None,
            param_sets=[{}],
        )

    def test_should_confirm_execution_on_name_hint(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            module_path = self._write_module(tmpdir)
            suggestion = self._suggestion(module_path, "delete_temp")
            self.assertTrue(tests_creator._should_confirm_execution(suggestion))

    def test_should_confirm_execution_on_body_hint(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            module_path = self._write_module(tmpdir)
            harmless = self._suggestion(module_path, "describe")
            destructive = self._suggestion(module_path, "clean_directory")

            self.assertFalse(tests_creator._should_confirm_execution(harmless))
            self.assertTrue(
                tests_creator._function_body_has_destructive_calls(str(module_path), "clean_directory")
            )
            self.assertTrue(tests_creator._should_confirm_execution(destructive))

    def test_crud_scenario_executes_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pkg = Path(tmpdir) / "crudpkg"
            pkg.mkdir()
            (pkg / "__init__.py").write_text("STATE = set()\n", encoding="utf-8")
            module_path = pkg / "storage.py"
            module_path.write_text(
                """
STATE = set()


def get_item(name, dry_run=False):
    return name in STATE


def create_item(name, dry_run=False):
    if not dry_run:
        STATE.add(name)
        return True
    return False


def delete_item(name, dry_run=False):
    if not dry_run:
        STATE.discard(name)
        return True
    return False
""",
                encoding="utf-8",
            )

            sys.path.insert(0, tmpdir)
            try:
                funcs = scanner.scan_python_functions(tmpdir)
                create_func = next(f for f in funcs if f.qualname == "create_item")
                suggestion = param_suggestor.suggest_params(create_func)

                self.assertIsNotNone(suggestion.scenario)
                os.environ["GHTEST_ASSUME_SAFE"] = "1"

                cassette_dir = Path(tmpdir) / "cassettes"
                test_obj = tests_creator.make_test_function(suggestion, cassette_dir=str(cassette_dir))
                try:
                    result = test_obj.test_callable()
                finally:
                    os.environ.pop("GHTEST_ASSUME_SAFE", None)
                self.assertTrue(result.cases)  # scenario appended
                scenario = suggestion.scenario
                assert scenario is not None
                scenario_cases = result.cases[-len(scenario.steps):]
                self.assertTrue(all(case.exception is None for case in scenario_cases))
            finally:
                sys.path.remove(tmpdir)


if __name__ == "__main__":
    unittest.main()
