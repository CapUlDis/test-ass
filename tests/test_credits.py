import pytest
from unittest import mock
from flask import current_app
from credit import check_user_with_password_exists, logger


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
def test_check_user_with_password_exists_normal_cases(app, set_db, name, password, result):
    with app.app_context():
        assert check_user_with_password_exists(name, password) is result

def test_check_user_with_password_exists_no_result(app):
    with mock.patch.object(logger, 'info') as mock_info:
        with app.app_context():
            assert check_user_with_password_exists('foo', 'bar') is False
        assert 'NoResultFound: no such username in database' in mock_info.call_args[0][0]

def test_check_user_with_password_exists_multiple_result(app, set_db):
    with pytest.raises(LookupError):
        with mock.patch.object(logger, 'error') as mock_error:
            with app.app_context():
                check_user_with_password_exists('foo', 'bar')
                assert 'MultipleResultsFound: database has more than one users with such name' in mock_error.call_args[0][0]
                