import pytest

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