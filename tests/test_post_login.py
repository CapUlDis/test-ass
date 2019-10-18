import requests
import pytest

def test_correct_login():
    
    response = requests.post('http://localhost:5000/login', json={"name" : "denchik", "password" : "foobar"})
    assert response.status_code == 200
    assert response.content == b'OK'

def test_incorrect_login():

    response = requests.post('http://localhost:5000/login', json={"name" : "den", "password" : "foobar"})
    assert response.status_code == 403
    assert response.content == b'FORBIDDEN'

def test_invalid_header():

    response = requests.post('http://localhost:5000/login', data={"name" : "den", "password" : "foobar"})
    assert response.status_code == 400
    assert response.content == b'BAD REQUEST'


