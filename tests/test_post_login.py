import pytest
import json

@pytest.mark.parametrize(
        ('datam', 'header', 'message'),
        (
                ('', '', b'Content-Type is not json.'),
                ('', {'content-type': 'xml'}, b'Content-Type is not json.'),
                ('smthg', {'content-type': 'application/json'}, b'Data is not in json format.'),
                (json.dumps({"exp1": "exp2", "exp3": "exp4"}), {'content-type': 'application/json'}, b'Name or/and password are missing.'),
                (json.dumps({"name": "denchik", "password": "foobar"}), {'content-type': 'application/json'}, b'Correct name and password.'),
                (json.dumps({"name": "den", "password": "foobar"}), {'content-type': 'application/json'}, b'Wrong name or password.'),
                (json.dumps({"name": "denchik", "password": "foo"}), {'content-type': 'application/json'}, b'Wrong name or password.'),
                
        ),
)
def test_login_with_different_data_headers(client, app, datam, header, message):
    response = client.post(
            '/login', data = datam, headers = header
            )
    
    assert message in response.data

    
