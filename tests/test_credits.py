import pytest
import os
import mock
from credit import load_credits, logger


@pytest.mark.parametrize(
    ('path', 'expected_str'),
    (
        (os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/credential.txt', f'FileNotFoundError: no credentials.txt in {os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}'),
        (os.path.dirname(os.path.realpath(__file__)) + '/crap.txt', f'JSONDecodeError: data in credentials.txt is not json'),
    ),
    ids = ['No credentials.txt case', 'Data in file is not json']
)
def test_load_credits_FileNotFound(path, expected_str):
    with mock.patch.object(logger, 'error') as mock_error:
        load_credits(path)
        mock_error.assert_called_once_with(expected_str)
        


    