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

def test_create_repo_case_14():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'name': 'coron', 'vb': 1}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_14.yaml'
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


def test_create_repo_case_15():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'name': 'coron', 'vb': 2}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_15.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='create_repo', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = _load_data('test_create_repo_case_15_stdout_29.py')
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'None', 'type': 'NoneType', 'value': None}
    assert_return_summary(result.return_summary, expected_return_summary, target='create_repo')


def test_create_repo_case_16():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'name': 'coron', 'vb': 3}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_16.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='create_repo', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = _load_data('test_create_repo_case_16_stdout_30.py')
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'None', 'type': 'NoneType', 'value': None}
    assert_return_summary(result.return_summary, expected_return_summary, target='create_repo')


def test_create_repo_case_17():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'name': 'coron', 'user': None}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_17.yaml'
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


def test_create_repo_case_18():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'name': 'coron', 'vb': 'example'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_18.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='create_repo', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is not None
    assert result.exception.__class__.__module__ + '.' + result.exception.__class__.__name__ == 'builtins.TypeError'
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'None', 'type': 'NoneType', 'value': None}
    assert_return_summary(result.return_summary, expected_return_summary, target='create_repo')


def test_create_repo_case_19():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'name': 'coron', 'user': 'example'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_19.yaml'
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


def test_delete_repo_case_0():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'dry_run': False, 'name': 'coron', 'vb': 1}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.delete_repo.case_0.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='delete_repo', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = True
    assert result.return_value == expected_return
    expected_output = 'coron deleted\n'
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'),
     ('/Users/kgregorian/.env/.env', 'r'),
     ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'True', 'type': 'builtins.bool', 'value': True}
    assert_return_summary(result.return_summary, expected_return_summary, target='delete_repo')


def test_delete_repo_case_1():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.delete_repo.case_1.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='delete_repo', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'),
     ('/Users/kgregorian/.env/.env', 'r'),
     ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'None', 'type': 'NoneType', 'value': None}
    assert_return_summary(result.return_summary, expected_return_summary, target='delete_repo')


def test_delete_repo_case_2():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'name': 'coron', 'user': 'gh4144'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.delete_repo.case_2.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='delete_repo', params=params, volatile_return_fields=volatile_fields)
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
    assert_return_summary(result.return_summary, expected_return_summary, target='delete_repo')


def test_delete_repo_case_3():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'name': 'coron', 'user': 'gh4144_alt'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.delete_repo.case_3.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='delete_repo', params=params, volatile_return_fields=volatile_fields)
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
    assert_return_summary(result.return_summary, expected_return_summary, target='delete_repo')
