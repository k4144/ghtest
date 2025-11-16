import importlib.util
import os
import sys
import tempfile
import textwrap
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ghtest import tests_creator, tests_writer  # noqa: E402
from ghtest.test_utils import RunTestWithCassette, execute_function  # noqa: E402


def _load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)  # type: ignore[assignment]
    return module


class TestsWriterTests(unittest.TestCase):
    def test_write_module_with_inline_and_external_data(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pkg = Path(tmpdir) / "pkg"
            pkg.mkdir()
            (pkg / "__init__.py").write_text("", encoding="utf-8")
            module_path = pkg / "ops.py"
            module_path.write_text(
                textwrap.dedent(
                    """
                    def noisy(value):
                        print("value:", value)
                        return {"value": value, "items": list(range(50))}
                    """
                ),
                encoding="utf-8",
            )

            suggestion = tests_creator.SuggestedFunctionTests(
                module="pkg.ops",
                filepath=str(module_path),
                qualname="noisy",
                docstring=None,
                param_sets=[{"value": 5}],
            )
            sys.path.insert(0, tmpdir)
            try:
                case = execute_function("pkg.ops", str(module_path), "noisy", {"value": 5})
            finally:
                sys.path.remove(tmpdir)
            run = RunTestWithCassette(cassette_path="", cases=[case])

            output_dir = Path(tmpdir) / "generated_tests"
            result = tests_writer.write_test_modules(
                [tests_writer.TestArtifact(suggestion=suggestion, run=run)],
                output_dir=str(output_dir),
                max_cases_per_module=1,
                inline_char_limit=40,
            )

            self.assertEqual(len(result.test_modules), 1)
            self.assertFalse(result.scenario_modules)
            test_module_path = result.test_modules[0]
            self.assertTrue(test_module_path.exists())

            data_dir = output_dir / "data"
            data_files = list(data_dir.glob("*.py"))
            self.assertTrue(data_files, "Expected return/print data to be externalized")

            sys.path.insert(0, tmpdir)
            try:
                test_module = _load_module(test_module_path)
                test_funcs = [getattr(test_module, name) for name in dir(test_module) if name.startswith("test_")]
                self.assertEqual(len(test_funcs), 1)
                test_funcs[0]()  # should not raise
            finally:
                sys.path.remove(tmpdir)

    def test_writes_scenario_module_with_env_guard(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pkg = Path(tmpdir) / "pkg"
            pkg.mkdir()
            (pkg / "__init__.py").write_text("", encoding="utf-8")
            module_path = pkg / "storage.py"
            module_path.write_text(
                textwrap.dedent(
                    """
                    STATE = []


                    def read_item(name, dry_run=False):
                        return name in STATE


                    def create_item(name, dry_run=False):
                        if not dry_run:
                            STATE.append(name)
                        return True


                    def delete_item(name, dry_run=False):
                        if not dry_run and name in STATE:
                            STATE.remove(name)
                            return True
                        return False
                    """
                ),
                encoding="utf-8",
            )

            suggestion = tests_creator.SuggestedFunctionTests(
                module="pkg.storage",
                filepath=str(module_path),
                qualname="create_item",
                docstring=None,
                param_sets=[{"name": "demo", "dry_run": False}],
                scenario=tests_creator.CrudScenario(
                    resource="item",
                    identifier="demo",
                    steps=[
                        tests_creator.ScenarioStep(
                            module="pkg.storage",
                            filepath=str(module_path),
                            qualname="read_item",
                            params={"name": "demo", "dry_run": False},
                            expect="falsy",
                        ),
                        tests_creator.ScenarioStep(
                            module="pkg.storage",
                            filepath=str(module_path),
                            qualname="create_item",
                            params={"name": "demo", "dry_run": False},
                            expect="truthy",
                        ),
                        tests_creator.ScenarioStep(
                            module="pkg.storage",
                            filepath=str(module_path),
                            qualname="delete_item",
                            params={"name": "demo", "dry_run": False},
                            expect="truthy",
                            cleanup=True,
                        ),
                    ],
                ),
            )

            sys.path.insert(0, tmpdir)
            try:
                main_case = execute_function("pkg.storage", str(module_path), "create_item", {"name": "demo", "dry_run": False})
                scenario_cases = [
                    execute_function(step.module, step.filepath, step.qualname, step.params)
                    for step in suggestion.scenario.steps  # type: ignore[arg-type]
                ]
            finally:
                sys.path.remove(tmpdir)
    def test_captures_file_io_operations(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pkg = Path(tmpdir) / "pkg"
            pkg.mkdir()
            (pkg / "__init__.py").write_text("", encoding="utf-8")
            module_path = pkg / "files.py"
            module_path.write_text(
                textwrap.dedent(
                    """
                    from pathlib import Path


                    def touch(base):
                        target = Path(base) / "sample.txt"
                        with target.open("w") as fh:
                            fh.write("content")
                        with target.open("r") as fh:
                            return fh.read()
                    """
                ),
                encoding="utf-8",
            )

            suggestion = tests_creator.SuggestedFunctionTests(
                module="pkg.files",
                filepath=str(module_path),
                qualname="touch",
                docstring=None,
                param_sets=[{"base": tmpdir}],
            )

            sys.path.insert(0, tmpdir)
            try:
                case = execute_function("pkg.files", str(module_path), "touch", {"base": tmpdir})
            finally:
                sys.path.remove(tmpdir)
            run = RunTestWithCassette(cassette_path="", cases=[case])
            output_dir = Path(tmpdir) / "io_tests"
            result = tests_writer.write_test_modules(
                [tests_writer.TestArtifact(suggestion=suggestion, run=run)],
                output_dir=str(output_dir),
                inline_char_limit=200,
            )
            test_module_path = result.test_modules[0]

            sys.path.insert(0, tmpdir)
            try:
                module = _load_module(test_module_path)
                test_funcs = [getattr(module, name) for name in dir(module) if name.startswith("test_")]
                self.assertEqual(len(test_funcs), 1)
                test_funcs[0]()
            finally:
                sys.path.remove(tmpdir)

    def test_skips_scenario_module_when_not_recorded(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pkg = Path(tmpdir) / "pkg"
            pkg.mkdir()
            (pkg / "__init__.py").write_text("", encoding="utf-8")
            module_path = pkg / "ops.py"
            module_path.write_text(
                textwrap.dedent(
                    """
                    STATE = []


                    def read_item(name):
                        return name in STATE


                    def create_item(name):
                        STATE.append(name)
                        return True
                    """
                ),
                encoding="utf-8",
            )

            suggestion = tests_creator.SuggestedFunctionTests(
                module="pkg.ops",
                filepath=str(module_path),
                qualname="create_item",
                docstring=None,
                param_sets=[{"name": "demo"}],
                scenario=tests_creator.CrudScenario(
                    resource="item",
                    identifier="demo",
                    steps=[
                        tests_creator.ScenarioStep(
                            module="pkg.ops",
                            filepath=str(module_path),
                            qualname="read_item",
                            params={"name": "demo"},
                            expect="falsy",
                        ),
                        tests_creator.ScenarioStep(
                            module="pkg.ops",
                            filepath=str(module_path),
                            qualname="create_item",
                            params={"name": "demo"},
                            expect="truthy",
                        ),
                    ],
                ),
            )

            sys.path.insert(0, tmpdir)
            try:
                main_case = execute_function("pkg.ops", str(module_path), "create_item", {"name": "demo"})
            finally:
                sys.path.remove(tmpdir)

            run = RunTestWithCassette(cassette_path="", cases=[main_case])
            output_dir = Path(tmpdir) / "no_scenario_tests"
            result = tests_writer.write_test_modules(
                [tests_writer.TestArtifact(suggestion=suggestion, run=run)],
                output_dir=str(output_dir),
            )
            self.assertFalse(result.scenario_modules)
            self.assertEqual(len(result.test_modules), 1)

    def test_can_disable_return_summary_assertions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pkg = Path(tmpdir) / "pkg"
            pkg.mkdir()
            (pkg / "__init__.py").write_text("", encoding="utf-8")
            module_path = pkg / "values.py"
            module_path.write_text(
                textwrap.dedent(
                    """
                    class Wrapper:
                        def __init__(self, value):
                            self.value = value

                        def __repr__(self):
                            return f"Wrapper({self.value})"


                    def build(value):
                        return Wrapper(value)
                    """
                ),
                encoding="utf-8",
            )

            suggestion = tests_creator.SuggestedFunctionTests(
                module="pkg.values",
                filepath=str(module_path),
                qualname="build",
                docstring=None,
                param_sets=[{"value": 42}],
            )

            sys.path.insert(0, tmpdir)
            try:
                case = execute_function("pkg.values", str(module_path), "build", {"value": 42})
            finally:
                sys.path.remove(tmpdir)

            run = RunTestWithCassette(cassette_path="", cases=[case])
            output_dir = Path(tmpdir) / "repr_only_tests"
            result = tests_writer.write_test_modules(
                [tests_writer.TestArtifact(suggestion=suggestion, run=run)],
                output_dir=str(output_dir),
                include_return_summary=False,
            )
            test_module_path = result.test_modules[0]
            contents = test_module_path.read_text(encoding="utf-8")
            self.assertNotIn("assert_return_summary", contents)
            self.assertNotIn("expected_return_summary", contents)

            sys.path.insert(0, tmpdir)
            try:
                module = _load_module(test_module_path)
                test_funcs = [getattr(module, name) for name in dir(module) if name.startswith("test_")]
                self.assertEqual(len(test_funcs), 1)
                test_funcs[0]()
            finally:
                sys.path.remove(tmpdir)


if __name__ == "__main__":
    unittest.main()
