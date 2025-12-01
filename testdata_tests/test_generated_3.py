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

def test_list_repos_case_7():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {'max_repos': 31}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.list_repos.case_7.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='list_repos', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_7_return_18.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = _load_data('test_list_repos_case_7_return_summary_19.py')
    assert_return_summary(result.return_summary, expected_return_summary, target='list_repos')


def test_list_repos_case_8():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {'vb': 2}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.list_repos.case_8.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='list_repos', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_8_return_20.py')
    assert result.return_value == expected_return
    expected_output = ('link:, page:1, nxt: False, url: '
     'https://api.github.com/user/repos?per_page=30&page=1\n')
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = _load_data('test_list_repos_case_8_return_summary_21.py')
    assert_return_summary(result.return_summary, expected_return_summary, target='list_repos')


def test_list_repos_case_9():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {'vb': 3}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.list_repos.case_9.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='list_repos', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_9_return_22.py')
    assert result.return_value == expected_return
    expected_output = ('link:, page:1, nxt: False, url: '
     'https://api.github.com/user/repos?per_page=30&page=1\n')
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = _load_data('test_list_repos_case_9_return_summary_23.py')
    assert_return_summary(result.return_summary, expected_return_summary, target='list_repos')


def test_list_repos_case_10():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {'user': None}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.list_repos.case_10.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='list_repos', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_10_return_24.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = _load_data('test_list_repos_case_10_return_summary_25.py')
    assert_return_summary(result.return_summary, expected_return_summary, target='list_repos')


def test_list_repos_case_11():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {'dry_run': None}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.list_repos.case_11.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='list_repos', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = _load_data('test_list_repos_case_11_return_26.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = _load_data('test_list_repos_case_11_return_summary_27.py')
    assert_return_summary(result.return_summary, expected_return_summary, target='list_repos')


def test_list_repos_case_12():
    func = import_function('gh_api', 'testdata/gh_api.py', 'list_repos')
    params = {'vb': 'example'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.list_repos.case_12.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='list_repos', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is not None
    assert result.exception.__class__.__module__ + '.' + result.exception.__class__.__name__ == 'builtins.TypeError'
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'None', 'type': 'NoneType', 'value': None}
    assert_return_summary(result.return_summary, expected_return_summary, target='list_repos')


def test_create_repo_case_0():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'dry_run': False, 'name': 'coron', 'vb': 1}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_0.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='create_repo', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = True
    assert result.return_value == expected_return
    expected_output = 'coron created\n'
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'True', 'type': 'builtins.bool', 'value': True}
    assert_return_summary(result.return_summary, expected_return_summary, target='create_repo')


def test_create_repo_case_1():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'dry_run': False, 'name': 'coron6', 'vb': 2}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_1.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='create_repo', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = False
    assert result.return_value == expected_return
    expected_output = _load_data('test_create_repo_case_1_stdout_28.py')
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'False', 'type': 'builtins.bool', 'value': False}
    assert_return_summary(result.return_summary, expected_return_summary, target='create_repo')


def test_create_repo_case_2():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_2.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='create_repo', params=params, volatile_return_fields=volatile_fields)
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
    assert_return_summary(result.return_summary, expected_return_summary, target='create_repo')


def test_create_repo_case_3():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'name': 'coron', 'user': 'gh4144'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_3.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='create_repo', params=params, volatile_return_fields=volatile_fields)
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
    assert_return_summary(result.return_summary, expected_return_summary, target='create_repo')
