import pytest, os
from unittest import mock
from auth import load_token_key, TokenGenerator, logger
from freezegun import freeze_time
from datetime import datetime, timedelta



@pytest.mark.parametrize(
    ('error', 'path', 'expected_str'),
    (
        (FileNotFoundError, 'token_keys.txt', 'FileNotFoundError: no credentials.txt in'),
        (TypeError, os.path.dirname(os.path.realpath(__file__)) + '/token_key_not_JWK_object.txt', 'is not JWK object')
    ),
    ids = ['No token key file case', 'Data in token key file is not JWK object']
)
def test_load_token_key_for_errors(error, path, expected_str):
    with pytest.raises(error):
        with mock.patch.object(logger, 'error') as mock_error:
            load_token_key(path)
    assert expected_str in mock_error.call_args[0][0]

def test_load_key_normal_case():
    test_token_key = load_token_key(os.path.dirname(os.path.realpath(__file__)) + '/test_token_key.txt')
    assert test_token_key.export() == '{"k":"foo","kty":"oct"}'

def test_class_TokenGenerator_create_and_check_token_normal_case():
    test_token_object  = TokenGenerator(os.path.dirname(os.path.realpath(__file__)) + '/test_token_key.txt')
    str_token = test_token_object.create_new_token('testname', 30)
    assert test_token_object.check_token(str_token) is True

def test_class_TokenGenerator_check_token_expired_token():
    test_token_object = TokenGenerator(os.path.dirname(os.path.realpath(__file__)) + '/test_token_key.txt')
    expired_token = test_token_object.create_new_token('testname', 30)
    with freeze_time(datetime.utcnow() + timedelta(minutes = 31)):
        with mock.patch.object(logger, 'info') as mock_info:
            assert test_token_object.check_token(expired_token) is False
            assert 'JWTExpired: token is expired' in mock_info.call_args[0][0]

def test_class_TokenGenerator_check_token_invalid_signature():
    main_token_object = TokenGenerator(os.path.dirname(os.path.realpath(__file__)) + '/test_token_key.txt')
    other_token_object = TokenGenerator(os.path.dirname(os.path.realpath(__file__)) + '/other_test_token_key.txt')
    token_with_invalid_signature = other_token_object.create_new_token('testname', 30)
    with mock.patch.object(logger, 'info') as mock_info:
        assert main_token_object.check_token(token_with_invalid_signature) is False
        assert 'InvalidJWSSignature: token has invalid signature' in mock_info.call_args[0][0]

@pytest.mark.parametrize(
    ('invalid_token_string', 'logger_message'),
    (
        ('this_string_is_not_JSON_Web_token', 'ValueError: received string is not JSON Web Token'),
        ('Bearer eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzY2NjMwNTUsInVzZXIiOiJkZW5jaGlrIn0.2NcVvhXPkNCmHMKa2DE4ugVImklZEgI6GWOjN3UY-B4', 'InvalidJWSObject: invalid token format')
    ),
    ids = ['Received string is not JSON Web Token', 'Invalid token format']
)
def test_class_TokenGenerator_check_token_invalid_data_format(invalid_token_string, logger_message):
    test_token_object = TokenGenerator(os.path.dirname(os.path.realpath(__file__)) + '/test_token_key.txt')
    with mock.patch.object(logger, 'info') as mock_info:
        assert test_token_object.check_token(invalid_token_string) is False
        assert logger_message in mock_info.call_args[0][0]

