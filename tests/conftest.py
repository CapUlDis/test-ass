import pytest
import os
from main import create_app, login


@pytest.fixture
def app():
    os.environ['todoappcredits'] = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/credentials.txt'
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    app.testing = True
    return app.test_client()