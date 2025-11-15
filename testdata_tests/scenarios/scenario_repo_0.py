import os

from ghtest.test_utils import call_with_capture, import_function

_SCENARIO_ENV = "GHTEST_RUN_SCENARIOS"

import importlib.util
from pathlib import Path

def _load_data(filename: str):
    data_path = Path(__file__).with_name('data') / filename
    spec = importlib.util.spec_from_file_location(f'{__name__}.{filename}', data_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.DATA

def test_repo_scenario_case_0():
    if os.environ.get(_SCENARIO_ENV) != '1':
        raise RuntimeError('Scenario tests disabled; set GHTEST_RUN_SCENARIOS=1 to execute them.')
    # Ensure resource does not exist before creation.
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'dry_run': False, 'name': 'repl1yky7'}
    result = call_with_capture(func, target='get_repo_data', params=params)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = 'repl1yky7 not found\n'
    assert result.printed == expected_output
    # Create resource instance.
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'dry_run': False, 'name': 'repl1yky7'}
    result = call_with_capture(func, target='create_repo', params=params)
    assert result.exception is None
    expected_return = True
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    # Validate resource exists after creation.
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'dry_run': False, 'name': 'repl1yky7'}
    result = call_with_capture(func, target='get_repo_data', params=params)
    assert result.exception is None
    expected_return = _load_data('test_repo_scenario_case_0_step_2_return_12.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    # Delete the resource to leave no residue.
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'dry_run': False, 'force': True, 'name': 'repl1yky7'}
    result = call_with_capture(func, target='delete_repo', params=params)
    assert result.exception is None
    expected_return = True
    assert result.return_value == expected_return
    expected_output = 'repl1yky7 deleted\n'
    assert result.printed == expected_output
    # Ensure resource is gone after deletion.
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'dry_run': False, 'name': 'repl1yky7'}
    result = call_with_capture(func, target='get_repo_data', params=params)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = 'repl1yky7 not found\n'
    assert result.printed == expected_output
