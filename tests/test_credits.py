import pytest
from unittest import mock
from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import and_
from alembic import command
from credit import check_user_with_password_exists, logger, check_useremail_exist, add_new_user_to_db
from models import User
from .test_migrations import alembic_cfg


@pytest.fixture()
def del_table_users_and_return_after_test():
    command.downgrade(alembic_cfg, 'base')
    yield None
    command.upgrade(alembic_cfg, 'head')

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

def test_check_user_with_password_exists_missing_db(app):
    with pytest.raises(ConnectionError):
        with mock.patch.object(logger, 'error') as mock_error:
            with app.app_context():
                current_app.engine = create_engine('postgresql://todoapp_user@localhost/missing_db')
                current_app.Session = sessionmaker(bind=current_app.engine)
                check_user_with_password_exists('foo', 'bar')
                assert 'OperationalError: database does not exist' in mock_error.call_args[0][0]

def test_check_user_with_password_exists_missing_table(app, del_table_users_and_return_after_test):
    with pytest.raises(NameError):
        with mock.patch.object(logger, 'error') as mock_error:
            with app.app_context():
                check_user_with_password_exists('foo', 'bar')
                assert 'ProgrammingError: table users does not exist' in mock_error.call_args[0][0]

@pytest.mark.parametrize(
    ('useremail', 'result'),
    (
        ('foo@bar.baz', True),
        ('foo@bad.baz', False)
    ),
    ids = ['Existing email', 'Non-existing email']
)
def test_check_useremail_exist_true_case(app, set_db, useremail, result):
    assert check_useremail_exist(useremail) is result

def test_check_useremail_missing_db(app):
    with pytest.raises(ConnectionError):
        with mock.patch.object(logger, 'error') as mock_error:
            with app.app_context():
                current_app.engine = create_engine('postgresql://todoapp_user@localhost/missing_db')
                current_app.Session = sessionmaker(bind=current_app.engine)
                check_useremail_exist('foo@bar.baz')
                assert 'OperationalError: database does not exist' in mock_error.call_args[0][0]

def test_check_useremail_missing_table(app, del_table_users_and_return_after_test):
    with pytest.raises(NameError):
        with mock.patch.object(logger, 'error') as mock_error:
            with app.app_context():
                check_useremail_exist('foo@bar.baz')
                assert 'ProgrammingError: table users does not exist' in mock_error.call_args[0][0]

def test_add_new_user_to_db(app):
    with app.app_context():
        add_new_user_to_db('foo', 'test_pwhash', 'bar@bax.ru')
        test_session = current_app.Session()
        assert test_session.query(exists().where(and_(User.name == 'foo', User.useremail == 'bar@bax.ru'))).scalar()