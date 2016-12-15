# -*- coding: utf-8 -*-
"""Test the echo server functionality."""
from email.utils import formatdate
import pytest


@pytest.fixture
def message_return():
    """Return the correct HTTP response messages."""
    from server import response_ok, response_error
    ok_message = 'HTTP/1.1 200 OK\r\nDate: '
    ok_message += formatdate(timeval=None, localtime=False, usegmt=True)
    ok_message += '\r\nThis is a minimal response\r\n'
    ok_message.encode('utf8')
    error_message = '500 Internal Server Error'
    error_message.encode('utf8')
    return response_error(), response_ok()


def test_client():
    """Test the client echo."""
    from client import client
    error_message, ok_message = message_return()
    assert client('short') == ok_message
    assert client('blah') == ok_message
    assert client('') == ok_message
    assert client('88888888') == ok_message

    # assert client('±¥Ä') == ok_message


def test_response_ok():
    """Test response_ok function."""
    from server import response_ok
    error_message, ok_message = message_return()
    assert response_ok() == ok_message


def test_response_error():
    """Test resposne_error function."""
    from server import response_error
    error_message, ok_message = message_return()
    assert response_error() == error_message
