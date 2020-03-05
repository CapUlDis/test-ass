import pytest
import os


os.environ['TDA_DB'] = 'postgresql://todoapp_user:tdapp8@localhost/todoapp_test'
os.environ['TDA_CREDITS'] = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/credentials.txt'
os.environ['TDA_TOKEN_KEY'] = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/token_key.txt'
os.environ['TDA_TOKEN_EXPIRATION_MINUTES'] = '30'


from main import create_app, login
from flask import current_app
from models import User



@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    app.testing = True
    return app.test_client()


@pytest.fixture()
def set_db(app):
    with app.app_context():
        try:
            test_session = current_app.Session()
            test_user_1 = User(name='denchik', passwordhash='pbkdf2:sha256:150000$wHwsgiLd$6979f267446c0e3d2797c21006f9272c3e19d5c70925d87989983ab3826350d8', useremail='foo@bar.baz')
            test_user_2 = User(name='foo', passwordhash='bar', useremail='baz')
            test_user_3 = User(name='bill', passwordhash='quux', useremail='bat')
            test_session.add_all([test_user_1, test_user_2, test_user_3])
            test_session.commit()
            yield None
            test_session.delete(test_user_1)
            test_session.delete(test_user_2)
            test_session.delete(test_user_3)
            test_session.commit()
        except:
            test_session.rollback()
            raise RuntimeError('App can not connect to database.')
        finally:
            test_session.close()