import pytest
import os
import mock
import re
from credit import load_credits, logger


@pytest.mark.parametrize(
    ('path', 'expected_str'),
    (
        (os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/credential.txt', 'to-do-app/credential.txt'),
        (os.path.dirname(os.path.realpath(__file__)) + '/crap.txt', 'data in credentials.txt is not json'),
    ),
    ids = ['No credentials.txt case', 'Data in file is not json']
)
def test_load_credits(path, expected_str):
    with mock.patch.object(logger, 'error') as mock_error:
        load_credits(path)
        assert re.search(expected_str, str(mock_error.mock_calls[0].args))



