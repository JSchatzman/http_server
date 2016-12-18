# -*- coding: utf-8 -*-
"""Test the echo server functionality."""
from email.utils import formatdate
import pytest
import os


@pytest.fixture
def test_import_functions(scope='module'):
    """Import functions needed to test."""
    from server import response_ok, response_error
    from client import client
    return client, response_ok, response_error


def test_create_valid_params_table():
    """Generate text for various return HTTP Responses."""
    client, response_ok, response_error = test_import_functions()
    message = 'HTTP/1.1 200 OK\r\nDate: '
    message += formatdate(timeval=None, localtime=False, usegmt=True)
    message += '\r\n\r\n'
    message.encode('utf8')
    python_request = 'GET requestfiles/sample.py HTTP/1.1\r\n'
    python_request += 'host: http://www.example.com\r\n\r\n'

    python_file = str(open('src/requestfiles/sample.py', 'r').read()).encode('utf8')

    text_request = 'GET requestfiles/sample.txt HTTP/1.1\r\n'
    text_request += 'host: http://www.example.com\r\n\r\n'

    text_file = str(open('src/requestfiles/sample.txt', 'r').read().encode('utf8'))

    html_request = 'GET requestfiles/sample.html HTTP/1.1\r\n'
    html_request += 'host: http://www.example.com\r\n\r\n'

    html_file = str(open('src/requestfiles/sample.html', 'r').read().encode('utf8'))

    image_file = str(open('src/requestfiles/images/russell.jpg',
                          'rb').read())

    image_request = 'GET requestfiles/images/russell.jpg HTTP/1.1\r\n'
    image_request += 'host: http://www.example.com\r\n\r\n'

    valid_params_table = [
        [python_request, response_ok(python_file)],
        [html_request, response_ok(html_file)],
      #  [image_request, response_ok(image_request)],
        [text_request, response_ok(text_file)]]

    return valid_params_table


@pytest.mark.parametrize("http_request, output", test_create_valid_params_table())
def test_client_valid(http_request, output):
    """Assert that different invalid requests are replied correctly."""
    client, response_ok, response_error = test_import_functions()
    assert client(http_request) == output


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

test_create_valid_params_table()