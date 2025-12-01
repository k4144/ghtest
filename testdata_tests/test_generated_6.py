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

def test_delete_repo_case_4():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'dry_run': False, 'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.delete_repo.case_4.yaml'
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


def test_delete_repo_case_5():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'dry_run': True, 'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.delete_repo.case_5.yaml'
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


def test_delete_repo_case_6():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'force': False, 'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.delete_repo.case_6.yaml'
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


def test_delete_repo_case_7():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'force': True, 'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.delete_repo.case_7.yaml'
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


def test_delete_repo_case_8():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'name': 'coron', 'vb': 0}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.delete_repo.case_8.yaml'
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


def test_delete_repo_case_9():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'name': 'coron', 'vb': 1}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.delete_repo.case_9.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='delete_repo', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = 'cant delete: coron not found\n'
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'),
     ('/Users/kgregorian/.env/.env', 'r'),
     ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'None', 'type': 'NoneType', 'value': None}
    assert_return_summary(result.return_summary, expected_return_summary, target='delete_repo')


def test_delete_repo_case_10():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'name': 'coron', 'vb': 2}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.delete_repo.case_10.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='delete_repo', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = _load_data('test_delete_repo_case_10_stdout_31.py')
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'),
     ('/Users/kgregorian/.env/.env', 'r'),
     ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'None', 'type': 'NoneType', 'value': None}
    assert_return_summary(result.return_summary, expected_return_summary, target='delete_repo')


def test_delete_repo_case_11():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'name': 'coron', 'vb': 3}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.delete_repo.case_11.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='delete_repo', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = None
    assert result.return_value == expected_return
    expected_output = _load_data('test_delete_repo_case_11_stdout_32.py')
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'),
     ('/Users/kgregorian/.env/.env', 'r'),
     ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'None', 'type': 'NoneType', 'value': None}
    assert_return_summary(result.return_summary, expected_return_summary, target='delete_repo')


def test_delete_repo_case_12():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'name': 'coron', 'user': None}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.delete_repo.case_12.yaml'
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


def test_delete_repo_case_13():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'name': 'coron', 'vb': 'example'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.delete_repo.case_13.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='delete_repo', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is not None
    assert result.exception.__class__.__module__ + '.' + result.exception.__class__.__name__ == 'builtins.TypeError'
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'None', 'type': 'NoneType', 'value': None}
    assert_return_summary(result.return_summary, expected_return_summary, target='delete_repo')
