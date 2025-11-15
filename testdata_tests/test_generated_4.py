from ghtest.test_utils import call_with_capture, import_function

import importlib.util
from pathlib import Path

def _load_data(filename: str):
    data_path = Path(__file__).with_name('data') / filename
    spec = importlib.util.spec_from_file_location(f'{__name__}.{filename}', data_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.DATA

def test_delete_repo_case_5():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'dry_run': True, 'name': 'coron7'}
    result = call_with_capture(func, target='delete_repo', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_delete_repo_case_6():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'force': False, 'name': 'coron7'}
    result = call_with_capture(func, target='delete_repo', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_delete_repo_case_7():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'force': True, 'name': 'coron7'}
    result = call_with_capture(func, target='delete_repo', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_delete_repo_case_8():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'name': 'coron7', 'vb': 0}
    result = call_with_capture(func, target='delete_repo', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_delete_repo_case_9():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'name': 'coron7', 'vb': 1}
    result = call_with_capture(func, target='delete_repo', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = 'cant delete: coron7 not found\n'
    assert result.printed == expected_output


def test_delete_repo_case_10():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'name': 'coron7', 'vb': 2}
    result = call_with_capture(func, target='delete_repo', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = _load_data('test_delete_repo_case_10_stdout_10.py')
    assert result.printed == expected_output


def test_delete_repo_case_11():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'name': 'coron7', 'vb': 3}
    result = call_with_capture(func, target='delete_repo', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = _load_data('test_delete_repo_case_11_stdout_11.py')
    assert result.printed == expected_output


def test_get_repo_data_case_0():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'dry_run': False, 'name': 'coron7', 'vb': 1}
    result = call_with_capture(func, target='get_repo_data', params=params)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = 'coron7 not found\n'
    assert result.printed == expected_output


def test_get_repo_data_case_1():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'dry_run': False, 'name': 'coron7', 'return_all': True, 'vb': 3}
    result = call_with_capture(func, target='get_repo_data', params=params)
    assert result.exception is None
    expected_return = <Response [404]>
    assert result.return_value == expected_return
    expected_output = ('user: gh4144\n'
     "headers: {'authorization': 'token github_pa..mU 99'}\n"
     'url: https://api.github.com/repos/gh4144/coron7\n')
    assert result.printed == expected_output


def test_get_repo_data_case_2():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron7'}
    result = call_with_capture(func, target='get_repo_data', params=params)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
