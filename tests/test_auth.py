import pytest, os
from unittest import mock
from auth import load_token_key, logger


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