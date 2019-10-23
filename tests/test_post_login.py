import pytest
import json

def test_login_json_without_content_type_header_returns_400(client, app):
    response = client.post('/login', 
            data = json.dumps({"name": "denchik", "password": "foobar"}),
            )
    print(response.data)
    assert response.data == b'Content-Type not json'

    
