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

def test_list_repos_case_4():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {'vb': 0}
    result = call_with_capture(func, target='list_repos', params=params)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_4_return_5.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_list_repos_case_5():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {'vb': 1}
    result = call_with_capture(func, target='list_repos', params=params)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_5_return_6.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_list_repos_case_6():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {'max_repos': 30}
    result = call_with_capture(func, target='list_repos', params=params)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_6_return_7.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_create_repo_case_0():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'dry_run': False, 'name': 'coron7', 'vb': 1}
    result = call_with_capture(func, target='create_repo', params=params)
    assert result.exception is None
    expected_return = True
    assert result.return_value == expected_return
    expected_output = 'coron7 created\n'
    assert result.printed == expected_output


def test_create_repo_case_1():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'dry_run': False, 'name': 'coron7', 'vb': 2}
    result = call_with_capture(func, target='create_repo', params=params)
    assert result.exception is None
    expected_return = False
    assert result.return_value == expected_return
    expected_output = _load_data('test_create_repo_case_1_stdout_8.py')
    assert result.printed == expected_output


def test_create_repo_case_2():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'name': 'coron7'}
    result = call_with_capture(func, target='create_repo', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_create_repo_case_3():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'name': 'coron7', 'user': 'gh4144'}
    result = call_with_capture(func, target='create_repo', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_create_repo_case_4():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'description': 'simple repo', 'name': 'coron7'}
    result = call_with_capture(func, target='create_repo', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_create_repo_case_5():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'name': 'coron7', 'private': True}
    result = call_with_capture(func, target='create_repo', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_create_repo_case_6():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'is_template': False, 'name': 'coron7'}
    result = call_with_capture(func, target='create_repo', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
