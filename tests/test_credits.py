import pytest
import os
from credit import load_credits, logger
from unittest import mock


@pytest.mark.parametrize(
    ('path', 'expected_str'),
    (
        (os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/credential.txt', 'to-do-app/credential.txt'),
        (os.path.dirname(os.path.realpath(__file__)) + '/crap.txt', 'data in credentials.txt is not json'),
        (os.path.dirname(os.path.realpath(__file__)) + '/not_dict.txt', 'Data in credentials.txt is not dictionary'),
    ),
    ids = ['No credentials.txt case', 'Data in file is not json', 'Data is not dictionary']
)
def test_load_credits(path, expected_str):
    with mock.patch.object(logger, 'error') as mock_error:
        load_credits(path)
        assert expected_str in mock_error.call_args[0][0]



