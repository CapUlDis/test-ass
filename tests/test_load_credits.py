import pytest
import os
from main import load_credits

@pytest.mark.parametrize(
    ('path_credit', 'expected'),
    (
        (os.path.dirname(os.path.realpath(__file__)) + '/credentials.txt', b'No such file or working directory'),
        (os.path.dirname(os.path.realpath(__file__)) + '/crap.txt', b'Data in credentials.txt is not json'),
    )
)
def test_load_credits_cases_exception(path_credit, expected):
    
    assert load_credits(path_credit) == expected