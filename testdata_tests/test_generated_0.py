import vcr
from ghtest.test_utils import assert_return_summary, call_with_capture, import_function

def test_get_commits_case_0():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'dry_run': False, 'name': 'coron', 'vb': 1}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_0.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_commits', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = 'repo not found\n'
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'None', 'type': 'NoneType', 'value': None}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_commits')


def test_get_commits_case_1():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'dry_run': False, 'name': 'coron6', 'vb': 1}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_1.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_commits', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = 0
    assert result.return_value == expected_return
    expected_output = 'Git Repository is empty.\n'
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': '0', 'type': 'builtins.int', 'value': 0}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_commits')


def test_get_commits_case_2():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'dry_run': False, 'name': 'coron234', 'vb': 1}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_2.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_commits', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = 'repo not found\n'
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'None', 'type': 'NoneType', 'value': None}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_commits')


def test_get_commits_case_3():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'max_commits': 50, 'name': 'example', 'return_all': True, 'vb': 1}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_3.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_commits', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = []
    assert result.return_value == expected_return
    expected_output = 'Git Repository is empty.\n'
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': '[]', 'type': 'builtins.list', 'value': []}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_commits')


def test_get_commits_case_4():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'max_commits': 'max', 'name': 'coron', 'return_all': True, 'vb': 3}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_4.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_commits', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = 'repo not found\n'
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'None', 'type': 'NoneType', 'value': None}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_commits')


def test_get_commits_case_5():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_5.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_commits', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'None', 'type': 'NoneType', 'value': None}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_commits')


def test_get_commits_case_6():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron', 'user': 'gh4144'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_6.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_commits', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'None', 'type': 'NoneType', 'value': None}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_commits')


def test_get_commits_case_7():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron', 'user': 'gh4144_alt'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_7.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_commits', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'None', 'type': 'NoneType', 'value': None}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_commits')


def test_get_commits_case_8():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'max_commits': 50, 'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_8.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_commits', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'None', 'type': 'NoneType', 'value': None}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_commits')


def test_get_commits_case_9():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'max_commits': 51, 'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_9.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_commits', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'None', 'type': 'NoneType', 'value': None}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_commits')
