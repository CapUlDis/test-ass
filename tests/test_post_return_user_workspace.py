import pytest, json
from main import logger
from unittest import mock


@pytest.mark.parametrize(
    ('headers', 'logger_message', 'returned_message', 'http_code'),
    (
        ('', 'In POST request Authorization header is missing', b'In POST request Authorization header is missing', 401),
        ({'Authorization': 'Bearer '}, 'In Authorization header token is missing', b'In Authorization header token is missing', 401),
        ({'Authorization': 'Bearer eyJhbGciOiJIJ9.eyJzdWIiOifQ.SflKxwQssw5c'}, 'Got invalid token', b'Please log in again', 401)
    ),
    ids = ['No header case', 'Empty header Authorization', 'Invalid token in header']
)
def test_return_user_workspace_error_cases(client, app, headers, logger_message, returned_message, http_code):
    with mock.patch.object(logger, 'info') as mock_info:
        response_error = client.post('/my-todos', headers = headers)
        assert logger_message in mock_info.call_args[0][0]
        assert returned_message in response_error.data
        assert http_code == response_error.status_code

def test_return_user_workspace_valid_token(client, app):
    response_login = client.post('/login', data = json.dumps({"name": "denchik", "password": "foobar"}), headers = {'content-type': 'application/json'})
    received_token = json.loads(response_login.data)
    response_return_user_workspace = client.post('/my-todos', headers = {'Authorization': received_token['token']})    
    assert 200 == response_return_user_workspace.status_code
    assert 'toDoLists' in str(response_return_user_workspace.data)


    
    
    
