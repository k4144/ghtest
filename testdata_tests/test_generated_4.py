import vcr
from ghtest.test_utils import assert_return_summary, call_with_capture, import_function

def test_create_repo_case_4():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'name': 'coron', 'user': 'gh4144_alt'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_4.yaml'
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


def test_create_repo_case_5():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'description': 'simple repo', 'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_5.yaml'
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


def test_create_repo_case_6():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'description': 'simple repo_alt', 'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_6.yaml'
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


def test_create_repo_case_7():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'name': 'coron', 'private': True}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_7.yaml'
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


def test_create_repo_case_8():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'name': 'coron', 'private': False}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_8.yaml'
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


def test_create_repo_case_9():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'is_template': False, 'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_9.yaml'
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


def test_create_repo_case_10():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'is_template': True, 'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_10.yaml'
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


def test_create_repo_case_11():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'dry_run': False, 'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_11.yaml'
    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')
    with vcr_recorder.use_cassette(cassette_path):
        result = call_with_capture(func, target='create_repo', params=params, volatile_return_fields=volatile_fields)
    assert result.exception is None
    expected_return = False
    assert result.return_value == expected_return
    expected_output = ''
    assert result.printed == expected_output
    expected_reads = [('/Users/kgregorian/.env/.env', 'r'), ('/Users/kgregorian/.env/.env', 'r')]
    assert result.file_reads == expected_reads
    expected_writes = []
    assert result.file_writes == expected_writes
    expected_return_summary = {'repr': 'False', 'type': 'builtins.bool', 'value': False}
    assert_return_summary(result.return_summary, expected_return_summary, target='create_repo')


def test_create_repo_case_12():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'dry_run': True, 'name': 'coron'}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_12.yaml'
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


def test_create_repo_case_13():
    func = import_function('gh_api', 'testdata/gh_api.py', 'create_repo')
    params = {'name': 'coron', 'vb': 0}
    volatile_fields = ['elapsed', 'headers']
    cassette_path = 'testdata_tests/cassettes/gh_api.create_repo.case_13.yaml'
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
