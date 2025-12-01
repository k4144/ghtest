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

def test_get_commits_case_10():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'dry_run': False, 'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_10.yaml'
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


def test_get_commits_case_11():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'dry_run': True, 'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_11.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_commits', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = _load_data('test_get_commits_case_11_return_0.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = _load_data('test_get_commits_case_11_return_summary_1.py')
    assert_return_summary(result.return_summary, expected_return_summary, target='get_commits')


def test_get_commits_case_12():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron', 'return_all': False}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_12.yaml'
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


def test_get_commits_case_13():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron', 'return_all': True}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_13.yaml'
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


def test_get_commits_case_14():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron', 'vb': 0}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_14.yaml'
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


def test_get_commits_case_15():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron', 'vb': 1}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_15.yaml'
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


def test_get_commits_case_16():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron', 'vb': 2}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_16.yaml'
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


def test_get_commits_case_17():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron', 'vb': 3}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_17.yaml'
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


def test_get_commits_case_18():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'name': 'coron', 'user': None}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_18.yaml'
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


def test_get_commits_case_19():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_commits')
    params = {'dry_run': None, 'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_commits.case_19.yaml'
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
