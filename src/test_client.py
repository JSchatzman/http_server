# -*- coding: utf-8 -*-
"""Test the echo server functionality."""
from email.utils import formatdate
import pytest


@pytest.fixture
def test_import_functions():
    """Import functions needed to test."""
    from server import response_ok, response_error
    from client import client
    return client, response_ok, response_error


def test_client_valid_request():
    """Test that correct response is returned if valid request."""
    client, response_ok, response_error = test_import_functions()
    response = 'HTTP/1.1 200 OK\r\nDate: '
    response += formatdate(timeval=None, localtime=False, usegmt=True)
    response += '\r\nThis is a minimal response\r\n'
    request = 'GET http://www.w3.org/pub/WWW/TheProject.html HTTP/1.1\r\n'
    request += 'host: http://www.example.com\r\n\r\n'
    assert client(request) == response_ok()


def test_create_error_params_table():
    """Generate text for various return error messages."""
    client, response_ok, response_error = test_import_functions()
    no_get = 'GAT http://www.w3.org/pub/WWW/TheProject.html HTTP/1.1\r\n'
    no_get += 'host: http://www.example.com\r\n\r\n'

    no_host = 'GET http://www.w3.org/pub/WWW/TheProject.html HTTP/1.1\r\n'
    no_host += 'hoos: http://www.example.com\r\n\r\n'

    wrong_version = 'GET http://www.w3.org/pub/WWW/TheProject.html HTTP/1.0\r\n'
    wrong_version += 'host: http://www.example.com\r\n\r\n'

    wrong_ending = 'GET http://www.w3.org/pub/WWW/TheProject.html HTTP/1.1\r\n'
    wrong_ending += 'host: http://www.example.com\r\n\r\n.'

    invalid_host = 'GET http://www.w3.org/pub/WWW/TheProject.html HTTP/1.1\r\n'
    invalid_host += 'host: httvp://www.example.com\r\n\r\n'

    malformed = 'blah'

    error_params_table = [
        [no_get, response_error(405)],
        [no_host, response_error('400 no host')],
        [wrong_version, response_error(505)],
        [wrong_ending, response_error('400 bad ending')],
        [invalid_host, response_error('400 invalid host')],
        [malformed, response_error('400 Bad Request')]]

    return error_params_table


@pytest.mark.parametrize("http_request, output", test_create_error_params_table())
def test_client_invalid(http_request, output):
    """Assert that different invalid requests are replied correctly."""
    client, response_ok, response_error = test_import_functions()
    assert client(http_request) == output


def test_parse_request_if_valid_request():
    """Request that the URI is return if valid request is made."""
    from server import parse_request
    request = 'GET http://www.w3.org/pub/WWW/TheProject.html HTTP/1.1\r\n'
    request += 'host: http://www.example.com\r\n\r\n'
    assert parse_request(request)[0] == 'http://www.w3.org/pub/WWW/TheProject.html'
