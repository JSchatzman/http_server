# -*- coding: utf-8 -*-
"""Test the echo server functionality."""
from email.utils import formatdate
import pytest


@pytest.fixture
def message_return():
    """Return the correct HTTP response messages."""
    from server import response_ok, response_error
    return response_error('test'), response_ok()


CLIENT_PARAMS_TABLE = [
    ['short'],
    ['blah'],
    ['±¥Ä'],
    [''],
    ['12345678']
]


@pytest.mark.parametrize('message', CLIENT_PARAMS_TABLE)
def test_client(message):
    """Test the client echo."""
    from client import client
    error_message, ok_message = message_return()
    assert client(str(message)) == ok_message


def test_response_ok():
    """Test response_ok function."""
    from server import response_ok
    error_message, ok_message = message_return()
    assert response_ok() == ok_message


def test_response_error():
    """Test resposne_error function."""
    from server import response_error
    error_message, ok_message = message_return()
    assert response_error('test') == error_message
