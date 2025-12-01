import vcr
from ghtest.test_utils import assert_return_summary, call_with_capture, import_function

def test_get_repo_data_case_9():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron', 'vb': 0}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_repo_data.case_9.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_repo_data', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': '{}', 'type': 'builtins.dict', 'value': {}}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_repo_data')


def test_get_repo_data_case_10():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron', 'vb': 1}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_repo_data.case_10.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_repo_data', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': '{}', 'type': 'builtins.dict', 'value': {}}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_repo_data')


def test_get_repo_data_case_11():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron', 'vb': 2}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_repo_data.case_11.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_repo_data', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': '{}', 'type': 'builtins.dict', 'value': {}}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_repo_data')


def test_get_repo_data_case_12():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron', 'vb': 3}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_repo_data.case_12.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_repo_data', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = ('user: gh4144\n'
     "headers: {'authorization': 'token github_pa..mU 99'}\n"
     'url: https://api.github.com/repos/gh4144/coron\n')
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': '{}', 'type': 'builtins.dict', 'value': {}}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_repo_data')


def test_get_repo_data_case_13():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron', 'user': None}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_repo_data.case_13.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_repo_data', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': '{}', 'type': 'builtins.dict', 'value': {}}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_repo_data')


def test_get_repo_data_case_14():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron', 'vb': 'example'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_repo_data.case_14.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_repo_data', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is not None
    assert result.exception.__class__.__module__ + '.' + result.exception.__class__.__name__ == 'builtins.TypeError'
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'None', 'type': 'NoneType', 'value': None}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_repo_data')
