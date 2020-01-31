import pytest
from unittest import mock
from flask import current_app
from credit import check_user_with_password_exists, logger
from models import User


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
def test_check_user_with_password_exists_normal_cases(app, name, password, result):
    with app.app_context():
        test_session = current_app.Session()
        test_user = User(name='denchik', passwordhash='pbkdf2:sha256:150000$wHwsgiLd$6979f267446c0e3d2797c21006f9272c3e19d5c70925d87989983ab3826350d8', useremail='foo@bar.baz')
        test_session.add(test_user)
        test_session.commit()
        assert check_user_with_password_exists(name, password) is result
        test_session.delete(test_user)
        test_session.commit()

def test_check_user_with_password_exists_no_result(app):
    with mock.patch.object(logger, 'info') as mock_info:
        with app.app_context():
            assert check_user_with_password_exists('foo', 'bar') is False
        assert 'NoResultFound: no such username in database' in mock_info.call_args[0][0]

def test_check_user_with_password_exists_multiple_result(app):
    with pytest.raises(LookupError):
        with mock.patch.object(logger, 'error') as mock_error:
            with app.app_context():
                test_session = current_app.Session()
                test_user_1 = User(name='foo', passwordhash='bar', useremail='baz')
                test_user_2 = User(name='foo', passwordhash='quux', useremail='bat')
                test_session.add_all([test_user_1, test_user_2])
                test_session.commit()    
                check_user_with_password_exists('foo', 'bar')
                assert 'MultipleResultsFound: database has more than one users with such name' in mock_error.call_args[0][0]
                test_session.delete(test_user_1)
                test_session.delete(test_user_2)
                test_session.commit()