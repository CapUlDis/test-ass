import pytest
import os
import mock



'''@pytest.mark.parametrize(
    ('path_credit', 'expected'),
    (
        (os.path.dirname(os.path.realpath(__file__)) + '/credentials.txt', b'No such file or working directory'),
        (os.path.dirname(os.path.realpath(__file__)) + '/crap.txt', b'Data in credentials.txt is not json'),
    )
)'''
def test_load_credits_cases_exception():
    with mock.patch('main.log') as log_mock:
        
    