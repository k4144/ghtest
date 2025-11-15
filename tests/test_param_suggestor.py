import atexit
import importlib.util
import os
import random
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

HISTORY_FILE = Path(tempfile.gettempdir()) / "ghtest_param_history_unittest.json"
if HISTORY_FILE.exists():
    HISTORY_FILE.unlink()
os.environ["GHTEST_PARAM_HISTORY"] = str(HISTORY_FILE)
atexit.register(lambda: HISTORY_FILE.exists() and HISTORY_FILE.unlink())

PARAM_DB_FILE = Path(tempfile.gettempdir()) / "ghtest_param_db_unittest.json"
if PARAM_DB_FILE.exists():
    PARAM_DB_FILE.unlink()
os.environ["GHTEST_PARAM_DB"] = str(PARAM_DB_FILE)
atexit.register(lambda: PARAM_DB_FILE.exists() and PARAM_DB_FILE.unlink())

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


param_suggestor = _load_module("test_param_suggestor_mod", PKG_DIR / "param_suggestor.py")
scanner = _load_module("test_scanner_mod", PKG_DIR / "scanner.py")


SAMPLE_MODULE = textwrap.dedent(
    """
    import math

    GH_API_TERM1 = "api-term"
    DEFAULT_LIMIT = 25
    VERBOSITY_LEVEL = 2


    def search(term, limit=DEFAULT_LIMIT, verbose=False):
        if verbose:
            print(term)
        return term, limit


    def lookup(term=GH_API_TERM1):
        return term


    def toggle(enabled=True):
        return enabled


    def talk(term, verbosity=1, vb=False):
        if vb:
            print(term)
        return term, verbosity, vb


    def validate_job(dry_run=True):
        return dry_run


    def run_job(dry_run=None):
        return dry_run


    def execute():
        run_job(dry_run=False)
        validate_job(dry_run=True)


    def get_widget(name, dry_run=True):
        return None if dry_run else {"name": name}


    def create_widget(name, dry_run=True):
        return not dry_run


    def delete_widget(name, dry_run=True):
        return not dry_run


    def report_status(vb=0):
        if vb:
            print(vb)
        if vb > 1:
            print("very verbose")
        return vb


    def format_name(name, suffix="!"):
        return name


    def raw_vb(vb):
        return vb


    if __name__ == "__main__":
        search(term="api-term", limit=10, verbose=True)
        lookup(term=GH_API_TERM1)
        talk(term="api-term", verbosity=VERBOSITY_LEVEL, vb=True)
        get_widget(name="demo", dry_run=True)
        create_widget(name="demo", dry_run=False)
        get_widget(name="demo", dry_run=False)
        delete_widget(name="demo", dry_run=False)
    """
)


class ModuleGlobalSuggestionTests(unittest.TestCase):
    def setUp(self) -> None:
        self._reset_history()
        self._reset_param_db()
        random.seed(0)

    def _reset_history(self):
        history_path = Path(os.environ["GHTEST_PARAM_HISTORY"])
        if history_path.exists():
            history_path.unlink()
        if hasattr(param_suggestor, "_PARAM_HISTORY_CACHE"):
            param_suggestor._PARAM_HISTORY_CACHE = None
        if hasattr(param_suggestor, "_PARAM_DB_CACHE"):
            param_suggestor._PARAM_DB_CACHE = None

    def _reset_param_db(self):
        db_path = Path(os.environ["GHTEST_PARAM_DB"])
        if db_path.exists():
            db_path.unlink()
        if hasattr(param_suggestor, "_PARAM_DB_CACHE"):
            param_suggestor._PARAM_DB_CACHE = None

    def _write_sample_module(self, tmpdir: str) -> Path:
        root = Path(tmpdir)
        pkg = root / "samplepkg"
        pkg.mkdir()
        (pkg / "__init__.py").write_text("", encoding="utf-8")
        module_path = pkg / "searcher.py"
        module_path.write_text(SAMPLE_MODULE, encoding="utf-8")
        return module_path

    def _scan_target(self, tmpdir: str, qualname: str = "search"):
        functions = scanner.scan_python_functions(tmpdir)
        for func in functions:
            if func.qualname == qualname:
                return func
        self.fail(f"{qualname} function not discovered by scanner")

    def test_scanner_collects_module_globals(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_sample_module(tmpdir)
            func = self._scan_target(tmpdir)

        self.assertIn("GH_API_TERM1", func.module_globals)
        self.assertEqual(func.module_globals["GH_API_TERM1"], "api-term")

    def test_param_suggestor_reuses_scanned_globals(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            module_path = self._write_sample_module(tmpdir)
            func = self._scan_target(tmpdir)
            os.remove(module_path)

            suggestions = param_suggestor.suggest_params(func)

        minimal = suggestions.param_sets[0]
        self.assertEqual(minimal["term"], "api-term")

    def test_optional_constant_is_used_verbatim(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_sample_module(tmpdir)
            func = self._scan_target(tmpdir, qualname="lookup")

            suggestions = param_suggestor.suggest_params(func)

        sets_with_term = [ps for ps in suggestions.param_sets if "term" in ps]
        self.assertTrue(any(ps["term"] == "api-term" for ps in sets_with_term))
        self.assertFalse(any(ps["term"] == "api-term_alt" for ps in sets_with_term))

    def test_parameter_usage_infers_literal_values(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_sample_module(tmpdir)
            func = self._scan_target(tmpdir, qualname="report_status")

            suggestions = param_suggestor.suggest_params(func, literal_only=True)

        vb_values = sorted({ps["vb"] for ps in suggestions.param_sets if "vb" in ps})
        self.assertEqual(vb_values, [0, 1, 2])

    def test_unused_optional_parameter_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_sample_module(tmpdir)
            func = self._scan_target(tmpdir, qualname="format_name")

            suggestions = param_suggestor.suggest_params(func, literal_only=True)

        self.assertTrue(all("suffix" not in ps for ps in suggestions.param_sets))

    def test_seed_database_values_used_for_required_param(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_sample_module(tmpdir)
            func = self._scan_target(tmpdir, qualname="raw_vb")

            suggestions = param_suggestor.suggest_params(func, literal_only=True)

        self.assertIn("vb", suggestions.param_sets[0])
        self.assertEqual(suggestions.param_sets[0]["vb"], 0)

    def test_disable_global_param_db_write_flag(self):
        original_db = os.environ.pop("GHTEST_PARAM_DB", None)
        original_state = os.environ.get("XDG_STATE_HOME")
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                os.environ["XDG_STATE_HOME"] = tmpdir
                os.environ["GHTEST_DISABLE_PARAM_DB_WRITE"] = "1"
                module_path = self._write_sample_module(tmpdir)
                func = self._scan_target(tmpdir, qualname="report_status")

                param_suggestor.suggest_params(func, literal_only=True)

                default_db = Path(tmpdir) / "ghtest" / "param_db.json"
                self.assertFalse(default_db.exists(), "Global cache should not be written when disabled")
        finally:
            if original_db is not None:
                os.environ["GHTEST_PARAM_DB"] = original_db
            else:
                os.environ.pop("GHTEST_PARAM_DB", None)
            if original_state is not None:
                os.environ["XDG_STATE_HOME"] = original_state
            else:
                os.environ.pop("XDG_STATE_HOME", None)
            os.environ.pop("GHTEST_DISABLE_PARAM_DB_WRITE", None)
            # ensure per-test temp DB is recreated for subsequent tests
            os.environ["GHTEST_PARAM_DB"] = str(PARAM_DB_FILE)
            self._reset_param_db()

    def test_literal_only_flag_disables_alternatives(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_sample_module(tmpdir)
            func = self._scan_target(tmpdir, qualname="lookup")

            suggestions = param_suggestor.suggest_params(func, literal_only=True)

        term_values = {ps["term"] for ps in suggestions.param_sets if "term" in ps}
        self.assertEqual(term_values, {"api-term"})

    def test_scanner_extracts_sample_calls_from_main_block(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_sample_module(tmpdir)
            func = self._scan_target(tmpdir, qualname="search")

        self.assertTrue(func.sample_calls, "Expected sample calls for search")
        sample_call = func.sample_calls[0]
        self.assertEqual(sample_call["limit"], 10)
        self.assertTrue(sample_call["verbose"])

    def test_sample_calls_feed_param_suggestions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_sample_module(tmpdir)
            func = self._scan_target(tmpdir, qualname="search")

            suggestions = param_suggestor.suggest_params(func)

        self.assertTrue(
            any(ps.get("limit") == 10 and ps.get("verbose") is True for ps in suggestions.param_sets),
            "Sample call should be part of suggestion set",
        )

    def test_boolean_default_infers_type(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_sample_module(tmpdir)
            func = self._scan_target(tmpdir, qualname="toggle")

            suggestions = param_suggestor.suggest_params(func)

        enabled_values = {ps["enabled"] for ps in suggestions.param_sets if "enabled" in ps}
        self.assertEqual(enabled_values, {True, False})

    def test_verbosity_parameters_generate_range(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_sample_module(tmpdir)
            func = self._scan_target(tmpdir, qualname="talk")

            suggestions = param_suggestor.suggest_params(func)

        verbosity_values = sorted(
            {ps["verbosity"] for ps in suggestions.param_sets if "verbosity" in ps}
        )
        self.assertTrue(
            all(val in verbosity_values for val in [0, 1, 2, 3]),
            f"Verbosity suggestions missing expected range: {verbosity_values}",
        )
        vb_values = {ps["vb"] for ps in suggestions.param_sets if "vb" in ps}
        self.assertEqual(vb_values, {False, True})

    def test_module_param_hints_shared_across_functions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_sample_module(tmpdir)
            func = self._scan_target(tmpdir, qualname="run_job")

            suggestions = param_suggestor.suggest_params(func)

        dry_run_values = {ps["dry_run"] for ps in suggestions.param_sets if "dry_run" in ps}
        self.assertTrue(dry_run_values <= {True, False})
        self.assertIn(False, dry_run_values)

    def test_crud_scenario_generated_for_create_function(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_sample_module(tmpdir)
            func = self._scan_target(tmpdir, qualname="create_widget")

            suggestion = param_suggestor.suggest_params(func)

        scenario = suggestion.scenario
        self.assertIsNotNone(scenario)
        assert scenario
        self.assertEqual(len(scenario.steps), 5)
        identifiers = {step.params.get("name") for step in scenario.steps if "name" in step.params}
        self.assertEqual(len(identifiers), 1)
        self.assertTrue(all(step.expect in {"truthy", "falsy"} for step in scenario.steps))

    def test_param_history_used_as_fallback(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_sample_module(tmpdir)
            func = self._scan_target(tmpdir, qualname="validate_job")
            param_suggestor.suggest_params(func)

        history_path = Path(os.environ["GHTEST_PARAM_HISTORY"])
        self.assertTrue(history_path.exists())

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pkg = root / "nextpkg"
            pkg.mkdir()
            (pkg / "__init__.py").write_text("", encoding="utf-8")
            module_path = pkg / "worker.py"
            module_path.write_text(
                "def process(dry_run=None):\n    return dry_run\n",
                encoding="utf-8",
            )
            funcs = scanner.scan_python_functions(tmpdir)
            func = next(f for f in funcs if f.qualname == "process")

            suggestions = param_suggestor.suggest_params(func)

        dry_run_values = {ps["dry_run"] for ps in suggestions.param_sets if "dry_run" in ps}
        self.assertIn(False, dry_run_values)

    def test_internal_call_values_prioritized(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_sample_module(tmpdir)
            func = self._scan_target(tmpdir, qualname="run_job")

            suggestions = param_suggestor.suggest_params(func)

        self.assertEqual(suggestions.param_sets[0].get("dry_run"), False)
        dry_run_values = {ps.get("dry_run") for ps in suggestions.param_sets if "dry_run" in ps}
        self.assertIn(False, dry_run_values)

    def test_scanner_ignores_ipynb_checkpoints(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            module_path = self._write_sample_module(tmpdir)
            checkpoints = module_path.parent / ".ipynb_checkpoints"
            checkpoints.mkdir()
            ckpt = checkpoints / "ghost-checkpoint.py"
            ckpt.write_text("def ghost():\n    return 42\n", encoding="utf-8")

            functions = scanner.scan_python_functions(tmpdir)

        self.assertFalse(any(f.qualname == "ghost" for f in functions))


if __name__ == "__main__":
    unittest.main()
