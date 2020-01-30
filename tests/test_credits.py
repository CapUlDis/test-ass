import pytest, os
from credit import check_user_with_password_exists, logger
from unittest import mock


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
        assert check_user_with_password_exists(name, password) is result