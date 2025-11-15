from ghtest.test_utils import call_with_capture, import_function

def test_get_commits_case_0():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'dry_run': False, 'name': 'coron7', 'vb': 1}
    result = call_with_capture(func, target='get_commits', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = 'repo not found\n'
    assert result.printed == expected_output


def test_get_commits_case_1():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'dry_run': False, 'name': 'coron7', 'vb': 1}
    result = call_with_capture(func, target='get_commits', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = 'repo not found\n'
    assert result.printed == expected_output


def test_get_commits_case_2():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'dry_run': False, 'name': 'coron7', 'vb': 1}
    result = call_with_capture(func, target='get_commits', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = 'repo not found\n'
    assert result.printed == expected_output


def test_get_commits_case_3():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'max_commits': 50, 'name': 'coron7', 'return_all': True, 'vb': 1}
    result = call_with_capture(func, target='get_commits', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = 'repo not found\n'
    assert result.printed == expected_output


def test_get_commits_case_4():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'max_commits': 'max', 'name': 'coron7', 'return_all': True, 'vb': 3}
    result = call_with_capture(func, target='get_commits', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = 'repo not found\n'
    assert result.printed == expected_output


def test_get_commits_case_5():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron7'}
    result = call_with_capture(func, target='get_commits', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_get_commits_case_6():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron7', 'user': False}
    result = call_with_capture(func, target='get_commits', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_get_commits_case_7():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron7', 'user': True}
    result = call_with_capture(func, target='get_commits', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_get_commits_case_8():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'max_commits': 50, 'name': 'coron7'}
    result = call_with_capture(func, target='get_commits', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output


def test_get_commits_case_9():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'dry_run': False, 'name': 'coron7'}
    result = call_with_capture(func, target='get_commits', params=params)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
