import pytest, os
from unittest import mock
from auth import load_token_key, Token, logger
from jwcrypto import jwt, jwk, jws
from freezegun import freeze_time


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

def test_class_Token_create_new_token_normal_case():
    test_token_object  = Token(os.path.dirname(os.path.realpath(__file__)) + '/test_token_key.txt')
    str_token = test_token_object.create_new_token('testname', 30)
    assert str_token.count('.') == 2

@pytest.mark.parametrize(
    ('token_exp', 'freeze_point', 'error', 'result'),
    (
        (30, 60, jwt.JWTExpired, False),
        (30, 0, jws.InvalidJWSSignature, )
    )
)    
def test_class_Tokem_check_token_all_cases(token_exp, error, result):
    str_token_wrong_key = ''

    test_token_object = Token(os.path.dirname(os.path.realpath(__file__)) + '/test_token_key.txt')
    str_token = test_token_object.create_new_token('testname', token_exp)
    test_token_object.check_token(str_token)
