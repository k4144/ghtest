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

def test_get_commits_case_10():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'dry_run': True, 'name': 'coron7'}
    result = call_with_capture(func, target='get_commits', params=params)
    assert result.exception is None
    expected_return = _load_data('test_get_commits_case_10_return_0.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_get_commits_case_11():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron7', 'return_all': False}
    result = call_with_capture(func, target='get_commits', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_get_commits_case_12():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron7', 'return_all': True}
    result = call_with_capture(func, target='get_commits', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_get_commits_case_13():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron7', 'vb': 0}
    result = call_with_capture(func, target='get_commits', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_get_commits_case_14():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron7', 'vb': 1}
    result = call_with_capture(func, target='get_commits', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = 'repo not found\n'
    assert result.printed == expected_output


def test_get_commits_case_15():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron7', 'vb': 2}
    result = call_with_capture(func, target='get_commits', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = 'repo not found\n'
    assert result.printed == expected_output


def test_list_repos_case_0():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {'max_repos': 30, 'vb': 1}
    result = call_with_capture(func, target='list_repos', params=params)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_0_return_1.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_list_repos_case_1():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {}
    result = call_with_capture(func, target='list_repos', params=params)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_1_return_2.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_list_repos_case_2():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {'user': False}
    result = call_with_capture(func, target='list_repos', params=params)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_2_return_3.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_list_repos_case_3():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {'user': True}
    result = call_with_capture(func, target='list_repos', params=params)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_3_return_4.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
