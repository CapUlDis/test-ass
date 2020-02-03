import pytest, json
from unittest import mock
from flask import current_app
from main import logger
from models import User


@pytest.fixture(autouse=True)
def set_db(app):
    with app.app_context():
        test_session = current_app.Session()
        test_user = User(name='denchik', passwordhash='pbkdf2:sha256:150000$wHwsgiLd$6979f267446c0e3d2797c21006f9272c3e19d5c70925d87989983ab3826350d8', useremail='foo@bar.baz')
        test_session.add(test_user)
        test_session.commit()
        yield None
        test_session.delete(test_user)
        test_session.commit()

@pytest.mark.parametrize(
        ('data', 'headers', 'logger_message', 'message', 'http_code'),
        (
                ('', '', 'In POST request Content-Type header is not json.', b'Content-Type is not json.', 400),
                ('', {'content-type': 'xml'}, 'In POST request Content-Type header is not json.', b'Content-Type is not json.', 400),
                ('smthg', {'content-type': 'application/json'}, 'Received data is not in json format', b'Data is not in json format.', 400),
                (json.dumps({"exp1": "exp2", "exp3": "exp4"}), {'content-type': 'application/json'}, 'In POST request name or/and password are missing.', b'Name or/and password are missing.', 400),
                (json.dumps({"name" : 78 , "password" : "bar" }), {'content-type': 'application/json'}, 'In POST request name is not a string.', b'Name is not a string.', 400),
                (json.dumps({"name" : "foo" , "password" : 55 }), {'content-type': 'application/json'}, 'In POST request password is not a string.', b'Password is not a string.', 400),
                (json.dumps({"name": "den", "password": "foobar"}), {'content-type': 'application/json'}, 'In POST request name or password is invalid.', b'Invalid name or password.', 403),
                (json.dumps({"name": "denchik", "password": "foo"}), {'content-type': 'application/json'}, 'In POST request name or password is invalid.', b'Invalid name or password.', 403),
                
        ),
        ids = ['No Content-Type','Content-Type is xml','Not json format','No password and data', 'Not string name', 'Not string password', 'Not registered name', 'Invalid password']
)
def test_login_with_invalid_data_and_headers(client, app, data, headers, logger_message, message, http_code):
        with mock.patch.object(logger, 'info') as mock_info:
                response = client.post(
                        '/login', data = data, headers = headers)
                
                assert logger_message in mock_info.call_args[0][0]
                assert message in response.data
                assert http_code == response.status_code

def test_login_with_valid_data_and_header(client, app):
        response = client.post(
                        '/login', data = json.dumps({"name": "denchik", "password": "foobar"}), headers = {'content-type': 'application/json'})
        
        assert b"token" in response.data
        assert 200 == response.status_code


        
