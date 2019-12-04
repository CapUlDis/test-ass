import pytest, os, json, logging
from credit import load_credits
from unittest import mock


logger = logging.getLogger('main.py')

@pytest.mark.parametrize(
    ('error','path', 'expected_str'),
    (
        (FileNotFoundError, os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/credential.txt', 'to-do-app/credential.txt'),
        (TypeError, os.path.dirname(os.path.realpath(__file__)) + '/crap.txt', 'data in credentials.txt is not json'),
        (TypeError, os.path.dirname(os.path.realpath(__file__)) + '/not_dict.txt', 'Data in credentials.txt is not dictionary'),
        (TypeError, os.path.dirname(os.path.realpath(__file__)) + '/not_string.txt', '2 keys and 2 values in credit dictionary are not string')
    ),
    ids = ['No credentials.txt case', 'Data in file is not json', 'Data is not dictionary', 'Credentials have not string data']
)
def test_load_credits(error, path, expected_str):
    with pytest.raises(error):
        with mock.patch.object(logger, 'error') as mock_error:
            load_credits(path)
            assert expected_str in mock_error.call_args[0][0]



