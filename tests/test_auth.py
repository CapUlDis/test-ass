import pytest, os
from unittest import mock
from auth import load_token_key, Token_gen, logger
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

def test_class_Token_create_and_check_token_normal_case():
    test_token_object  = Token_gen(os.path.dirname(os.path.realpath(__file__)) + '/test_token_key.txt')
    str_token = test_token_object.create_new_token('testname', 30)
    assert str_token.count('.') == 2
    assert test_token_object.check_token(str_token) is True

@pytest.mark.parametrize(
    ('n_case', 'expected_str'),
    (
        (0, 'JWTExpired: token is expired'),
        (1, 'InvalidJWSSignature: token has invalid signature'),
        (2, 'ValueError: received string is not JSON Web Token')
    ),
    ids = ['Expired token', 'Token has invalid signature', 'Received string is not JSON Web Token']
)    
def test_class_Tokem_check_token_all_error_cases(n_case, expected_str):
    token_case_list = [0,0,0]

    main_token_object = Token_gen(os.path.dirname(os.path.realpath(__file__)) + '/test_token_key.txt')
    token_case_list[0] = main_token_object.create_new_token('testname', 30)
    
    other_key_token_object = Token_gen(os.path.dirname(os.path.realpath(__file__)) + '/other_test_token_key.txt')
    token_case_list[1] = other_key_token_object.create_new_token('testname', 60)

    token_case_list[2] = 'this_string_is_not_JSON_Web_token'

    with freeze_time(datetime.utcnow() + timedelta(minutes = 31)):
        with mock.patch.object(logger, 'info') as mock_info:
            assert main_token_object.check_token(token_case_list[n_case]) is False
            assert expected_str in mock_info.call_args[0][0]
