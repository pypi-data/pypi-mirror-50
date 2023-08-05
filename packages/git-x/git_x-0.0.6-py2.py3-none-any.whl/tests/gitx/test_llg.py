import mock
import pytest

import utils
from gitx import Gitx


@mock.patch('gitx.call', return_value=0)
def test_llg_with_5_by_default(mock_call):
    Gitx().llg()
    expected = 'git log --oneline -n {}'.format(5)
    mock_call.assert_called_once_with(expected)


@mock.patch('gitx.call', return_value=0)
def test_llg_with_n(mock_call):
    n = 10
    Gitx().llg(n)
    expected = 'git log --oneline -n {}'.format(n)
    mock_call.assert_called_once_with(expected)


def test_llg_with_negative():
    with pytest.raises(Exception) as e:
        n = -1
        Gitx().llg(n)
        expected = 'The commit count must be greater than zero.'
        assert e == expected
