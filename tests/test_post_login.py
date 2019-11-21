import pytest
import json
import mock
import main

@pytest.mark.parametrize(
        ('data', 'headers', 'message', 'http_code'),
        (
                ('', '', b'Content-Type is not json.', 400),
                ('', {'content-type': 'xml'}, b'Content-Type is not json.', 400),
                ('smthg', {'content-type': 'application/json'}, b'Data is not in json format.', 400),
                (json.dumps({"exp1": "exp2", "exp3": "exp4"}), {'content-type': 'application/json'}, b'Name or/and password are missing.', 400),
                (json.dumps({"name": "denchik", "password": "foobar"}), {'content-type': 'application/json'}, b'Correct name and password.', 200),
                (json.dumps({"name": "den", "password": "foobar"}), {'content-type': 'application/json'}, b'Invalid name or password.', 403),
                (json.dumps({"name": "denchik", "password": "foo"}), {'content-type': 'application/json'}, b'Invalid name or password.', 403),
                
        ),
        ids = ['No Content-Type','Content-Type is xml','Not json format','No password and data','Correct name and password','Not registered name','Invalid password']
)
def test_login_with_different_data_and_headers(client, app, data, headers, message, http_code):
        response = client.post(
                '/login', data = data, headers = headers
                )
        
        assert message in response.data
        assert http_code == response.status_code


        
