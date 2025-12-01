import vcr
from ghtest.test_utils import assert_return_summary, call_with_capture, import_function

import importlib.util
from pathlib import Path

def _load_data(filename: str):
    data_path = Path(__file__).with_name('data') / filename
    spec = importlib.util.spec_from_file_location(f'{__name__}.{filename}', data_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.DATA

def test_get_commits_case_20():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron', 'vb': 'example'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_20.yaml'
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


def test_get_commits_case_21():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron', 'user': 'example'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_21.yaml'
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


def test_get_commits_case_22():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'dry_run': 'example', 'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_22.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_commits', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = _load_data('test_get_commits_case_22_return_2.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = _load_data('test_get_commits_case_22_return_summary_3.py')
    assert_return_summary(result.return_summary, expected_return_summary, target='get_commits')


def test_list_repos_case_0():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {'max_repos': 30, 'vb': 1}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.list_repos.case_0.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='list_repos', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_0_return_4.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = _load_data('test_list_repos_case_0_return_summary_5.py')
    assert_return_summary(result.return_summary, expected_return_summary, target='list_repos')


def test_list_repos_case_1():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.list_repos.case_1.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='list_repos', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_1_return_6.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = _load_data('test_list_repos_case_1_return_summary_7.py')
    assert_return_summary(result.return_summary, expected_return_summary, target='list_repos')


def test_list_repos_case_2():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {'user': 'gh4144'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.list_repos.case_2.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='list_repos', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_2_return_8.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = _load_data('test_list_repos_case_2_return_summary_9.py')
    assert_return_summary(result.return_summary, expected_return_summary, target='list_repos')


def test_list_repos_case_3():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {'user': 'gh4144_alt'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.list_repos.case_3.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='list_repos', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_3_return_10.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = _load_data('test_list_repos_case_3_return_summary_11.py')
    assert_return_summary(result.return_summary, expected_return_summary, target='list_repos')


def test_list_repos_case_4():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {'vb': 0}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.list_repos.case_4.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='list_repos', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_4_return_12.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = _load_data('test_list_repos_case_4_return_summary_13.py')
    assert_return_summary(result.return_summary, expected_return_summary, target='list_repos')


def test_list_repos_case_5():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {'vb': 1}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.list_repos.case_5.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='list_repos', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_5_return_14.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = _load_data('test_list_repos_case_5_return_summary_15.py')
    assert_return_summary(result.return_summary, expected_return_summary, target='list_repos')


def test_list_repos_case_6():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {'max_repos': 30}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.list_repos.case_6.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='list_repos', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_6_return_16.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = _load_data('test_list_repos_case_6_return_summary_17.py')
    assert_return_summary(result.return_summary, expected_return_summary, target='list_repos')
