import pytest, os
from credit import load_credits, Credits, logger
from unittest import mock


@pytest.mark.parametrize(
    ('error','path', 'expected_str'),
    (
        (FileNotFoundError, os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/credential.txt', 'to-do-app/credential.txt'),
        (TypeError, os.path.dirname(os.path.realpath(__file__)) + '/crap.txt', 'data in credentials.txt is not json'),
        (TypeError, os.path.dirname(os.path.realpath(__file__)) + '/not_dict.txt', 'Data in credentials.txt is not dictionary or malformed'),
        (TypeError, os.path.dirname(os.path.realpath(__file__)) + '/not_string.txt', '3 values in credit dictionary are not string')
    ),
    ids = ['No credentials.txt case', 'Data in file is not json', 'Data is not dictionary', 'Credentials have not string data']
)
def test_load_credits_errors(error, path, expected_str):
    with pytest.raises(error):
        with mock.patch.object(logger, 'error') as mock_error:
            load_credits(path)
    assert expected_str in mock_error.call_args[0][0]

def test_load_credits_normal():
    test_credit = load_credits(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/credentials.txt')
    assert test_credit == {"denchik": "pbkdf2:sha256:150000$wHwsgiLd$6979f267446c0e3d2797c21006f9272c3e19d5c70925d87989983ab3826350d8"}

@pytest.mark.parametrize(
    ('name', 'password', 'result'),
    (
        ('denchik', 'foobar', True),
        ('denchik', 'foo', False),
        ('den', 'foobar', False),
        ('den', 'foo', False),
    ),
    ids = ['Correct credentials', 'Invalid password', 'Invalid name', 'Invalid name and password']
)
def test_class_Credits(name, password, result):
    test_credit = Credits(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/credentials.txt')
    assert test_credit.check_user_with_password_exists(name, password) is result
    