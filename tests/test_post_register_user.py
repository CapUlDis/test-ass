import pytest, json
from unittest import mock
from flask import current_app
from alembic import command
from main import logger
from credit import check_name_exist
from .test_migrations import alembic_cfg


@pytest.mark.parametrize(
        ('data', 'headers', 'logger_message', 'message', 'http_code'),
        (
                ('', '', 'In POST request Content-Type header is not json.', b'Content-Type is not json.', 400),
                ('', {'content-type': 'xml'}, 'In POST request Content-Type header is not json.', b'Content-Type is not json.', 400),
                ('smthg', {'content-type': 'application/json'}, 'Received data is not in json format', b'Data is not in json format.', 400),
                (json.dumps({"exp1": "exp2", "exp3": "exp4"}), {'content-type': 'application/json'}, 'In POST request name or/and useremail are missing.', b'Name or/and useremail are missing.', 400),
                (json.dumps({"name" : 78 , "useremail" : "bar" }), {'content-type': 'application/json'}, 'In POST request name is not a string.', b'Name is not a string.', 400),
                (json.dumps({"name" : "foo" , "useremail" : 55 }), {'content-type': 'application/json'}, 'In POST request useremail is not a string.', b'Useremail is not a string.', 400),
                (json.dumps({"name": "denchik", "useremail": "foo@bar.baz"}), {'content-type': 'application/json'}, 'POST request name already exists in database.', b'User with such name is already registered.', 400),
                
        ),
        ids = ['No Content-Type','Content-Type is xml','Not json format','No name and useremail', 'Not string name', 'Not string useremail', 'Not registered name']
)
def test_register_user_invalid_data_and_headers(client, app, set_db, data, headers, logger_message, message, http_code):
        with mock.patch.object(logger, 'info') as mock_info:
                response = client.post(
                        '/register', data = data, headers = headers)
                
                assert logger_message in mock_info.call_args[0][0]
                assert message in response.data
                assert http_code == response.status_code

def test_register_user_valid_data_and_headers(client, app):
        with app.app_context():
                assert not check_name_exist('igor')
                response = client.post(
                                '/register', data = json.dumps({"name": "igor", "useremail": "ig@or.ru"}), headers = {'content-type': 'application/json'})
                
                assert b"token" in response.data
                assert b"newPassword" in response.data
                assert 200 == response.status_code
                assert check_name_exist('igor')
                command.downgrade(alembic_cfg, 'base')
                command.upgrade(alembic_cfg, 'head')