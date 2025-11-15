from ghtest.test_utils import call_with_capture, import_function

def test_get_repo_data_case_3():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron7', 'user': False}
    result = call_with_capture(func, target='get_repo_data', params=params)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_get_repo_data_case_4():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron7', 'user': True}
    result = call_with_capture(func, target='get_repo_data', params=params)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_get_repo_data_case_5():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron7', 'return_all': False}
    result = call_with_capture(func, target='get_repo_data', params=params)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_get_repo_data_case_6():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron7', 'return_all': True}
    result = call_with_capture(func, target='get_repo_data', params=params)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_get_repo_data_case_7():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'dry_run': False, 'name': 'coron7'}
    result = call_with_capture(func, target='get_repo_data', params=params)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = 'coron7 not found\n'
    assert result.printed == expected_output


def test_get_repo_data_case_8():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'dry_run': True, 'name': 'coron7'}
    result = call_with_capture(func, target='get_repo_data', params=params)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_get_repo_data_case_9():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron7', 'vb': 0}
    result = call_with_capture(func, target='get_repo_data', params=params)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_get_repo_data_case_10():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron7', 'vb': 1}
    result = call_with_capture(func, target='get_repo_data', params=params)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_get_repo_data_case_11():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron7', 'vb': 2}
    result = call_with_capture(func, target='get_repo_data', params=params)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_get_repo_data_case_12():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron7', 'vb': 3}
    result = call_with_capture(func, target='get_repo_data', params=params)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = ('user: gh4144\n'
     "headers: {'authorization': 'token github_pa..mU 99'}\n"
     'url: https://api.github.com/repos/gh4144/coron7\n')
    assert result.printed == expected_output
