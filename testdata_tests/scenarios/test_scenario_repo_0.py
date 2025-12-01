import os
import vcr

from ghtest.test_utils import assert_return_summary, call_with_capture, import_function

_SCENARIO_ENV = "GHTEST_RUN_SCENARIOS"
_SCENARIO_LIVE_ENV = "GHTEST_SCENARIO_LIVE"
_USE_RECORDED_CASSETTES = os.environ.get(_SCENARIO_LIVE_ENV) != '1'

import importlib.util
from pathlib import Path

def _load_data(filename: str):
    data_path = Path(__file__).parent.parent / 'data' / filename
    spec = importlib.util.spec_from_file_location(f'{__name__}.{filename}', data_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.DATA

def test_repo_scenario_case_0():
    # Scenario tests are now enabled by default
    pass
    # Ensure resource does not exist before creation.
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'dry_run': False, 'name': 'rep80vwl1'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.scenario.step_0.yaml'
    if _USE_RECORDED_CASSETTES:
        vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
        with vcr_recorder.use_cassette(cassette_path):
            result = call_with_capture(func, target='get_repo_data', params=params, volatile_return_fields=volatile_fields)
    else:
        result = call_with_capture(func, target='get_repo_data', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = 'rep80vwl1 not found\n'
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': '{}', 'type': 'builtins.dict', 'value': {}}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_repo_data')
    # Create resource instance.
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'dry_run': False, 'name': 'rep80vwl1'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.scenario.step_1.yaml'
    if _USE_RECORDED_CASSETTES:
        vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
        with vcr_recorder.use_cassette(cassette_path):
            result = call_with_capture(func, target='create_repo', params=params, volatile_return_fields=volatile_fields)
    else:
        result = call_with_capture(func, target='create_repo', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = True
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'True', 'type': 'builtins.bool', 'value': True}
    assert_return_summary(result.return_summary, expected_return_summary, target='create_repo')
    # Validate resource exists after creation.
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'dry_run': False, 'name': 'rep80vwl1'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.scenario.step_2.yaml'
    if _USE_RECORDED_CASSETTES:
        vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
        with vcr_recorder.use_cassette(cassette_path):
            result = call_with_capture(func, target='get_repo_data', params=params, volatile_return_fields=volatile_fields)
    else:
        result = call_with_capture(func, target='get_repo_data', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = _load_data('test_repo_scenario_case_0_step_2_return_34.py')
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = _load_data('test_repo_scenario_case_0_step_2_return_summary_35.py')
    assert_return_summary(result.return_summary, expected_return_summary, target='get_repo_data')
    # Delete the resource to leave no residue.
    func = import_function('gh_api', 'testdata/gh_api.py', 'delete_repo')
    params = {'dry_run': False, 'force': True, 'name': 'rep80vwl1'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.scenario.cleanup.yaml'
    if _USE_RECORDED_CASSETTES:
        vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
        with vcr_recorder.use_cassette(cassette_path):
            result = call_with_capture(func, target='delete_repo', params=params, volatile_return_fields=volatile_fields)
    else:
        result = call_with_capture(func, target='delete_repo', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = True
    assert result.return_value == expected_return
    expected_output = 'rep80vwl1 deleted\n'
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'),
     ('/Users/kgregorian/.env/.env', 'r'),
     ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'True', 'type': 'builtins.bool', 'value': True}
    assert_return_summary(result.return_summary, expected_return_summary, target='delete_repo')
    # Ensure resource is gone after deletion.
    func = import_function('gh_api', 'testdata/gh_api.py', 'get_repo_data')
    params = {'dry_run': False, 'name': 'rep80vwl1'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.scenario.step_4.yaml'
    if _USE_RECORDED_CASSETTES:
        vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
        with vcr_recorder.use_cassette(cassette_path):
            result = call_with_capture(func, target='get_repo_data', params=params, volatile_return_fields=volatile_fields)
    else:
        result = call_with_capture(func, target='get_repo_data', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = {}
    assert result.return_value == expected_return
    expected_output = 'rep80vwl1 not found\n'
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': '{}', 'type': 'builtins.dict', 'value': {}}
    assert_return_summary(result.return_summary, expected_return_summary, target='get_repo_data')
