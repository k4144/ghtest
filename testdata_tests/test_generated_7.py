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

def test_delete_repo_case_14():
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'name': 'coron', 'user': 'example'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.delete_repo.case_14.yaml'
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


def test_get_repo_data_case_0():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'dry_run': False, 'name': 'coron', 'vb': 1}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_repo_data.case_0.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_repo_data', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = 'coron not found\n'
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': '{}', 'type': 'builtins.dict', 'value': {}}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_repo_data')


def test_get_repo_data_case_1():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'dry_run': False, 'name': 'coron', 'return_all': True, 'vb': 3}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_repo_data.case_1.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_repo_data', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = '<Response [404]>'
    assert repr(result.return_value) == expected_return
    expected_output = ('user: gh4144\n'
     "headers: {'authorization': 'token github_pa..mU 99'}\n"
     'url: https://api.github.com/repos/gh4144/coron\n')
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = _load_data('test_get_repo_data_case_1_return_summary_33.py')
    assert_return_summary(result.return_summary, expected_return_summary, target='get_repo_data')


def test_get_repo_data_case_2():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_repo_data.case_2.yaml'
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


def test_get_repo_data_case_3():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron', 'user': 'gh4144'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_repo_data.case_3.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_repo_data', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': '{}', 'type': 'builtins.dict', 'value': {}}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_repo_data')


def test_get_repo_data_case_4():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron', 'user': 'gh4144_alt'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_repo_data.case_4.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_repo_data', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': '{}', 'type': 'builtins.dict', 'value': {}}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_repo_data')


def test_get_repo_data_case_5():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron', 'return_all': False}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_repo_data.case_5.yaml'
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


def test_get_repo_data_case_6():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'name': 'coron', 'return_all': True}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_repo_data.case_6.yaml'
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


def test_get_repo_data_case_7():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'dry_run': False, 'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_repo_data.case_7.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='get_repo_data', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = 'coron not found\n'
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': '{}', 'type': 'builtins.dict', 'value': {}}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_repo_data')


def test_get_repo_data_case_8():
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'dry_run': True, 'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.get_repo_data.case_8.yaml'
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
