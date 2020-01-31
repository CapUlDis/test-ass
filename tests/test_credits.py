import pytest
from credit import check_user_with_password_exists
from flask import current_app
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
def test_check_user_with_password_exists(app, name, password, result):
    with app.app_context():
        test_session = current_app.Session()
        test_user = User(name='denchik', passwordhash='pbkdf2:sha256:150000$wHwsgiLd$6979f267446c0e3d2797c21006f9272c3e19d5c70925d87989983ab3826350d8', useremail='foo@bar.baz')
        test_session.add(test_user)
        test_session.commit()
        assert check_user_with_password_exists(name, password) is result
        test_session.delete(test_user)
        test_session.commit()
