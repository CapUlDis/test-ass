import pytest
import os


os.environ['TDA_DB'] = 'postgresql://todoapp_user:tdapp8@localhost/todoapp_test'
os.environ['TDA_CREDITS'] = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/credentials.txt'
os.environ['TDA_TOKEN_KEY'] = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/token_key.txt'
os.environ['TDA_TOKEN_EXPIRATION_MINUTES'] = '30'


from main import create_app, login


@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    app.testing = True
    return app.test_client()