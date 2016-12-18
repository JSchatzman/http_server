# -*- coding: utf-8 -*-
"""Test the echo server functionality."""
from email.utils import formatdate
import pytest
import os



def test_create_valid_params_table():
    """Generate text for various return HTTP Responses."""
    from client import client
    from server import response_ok, response_error
    message = 'HTTP/1.1 200 OK\r\nDate: '
    message += formatdate(timeval=None, localtime=False, usegmt=True)
    message += '\r\n\r\n'
    message.encode('utf8')
    python_request = 'GET requestfiles/sample.py HTTP/1.1\r\n'
    python_request += 'host: http://www.example.com\r\n\r\n'

    python_file = b'#!/usr/bin/env python\n\n\ntest = [i for i in range(5)]'
    python_file += b'\nprint (test)\n'

    text_request = 'GET requestfiles/sample.txt HTTP/1.1\r\n'
    text_request += 'host: http://www.example.com\r\n\r\n'

    text_file = b'This is a sample text file.\nPython programming is '
    text_file += b'lots of fun.\nGO Hawks!\nGO Dawgs!'

    html_request = 'GET requestfiles/sample.html HTTP/1.1\r\n'
    html_request += 'host: http://www.example.com\r\n\r\n'

    html_file = b'<!DOCTYPE html>\n<html>\n<body>\n\n<h1>Sample '
    html_file += b'HTML</h1>\n\n<p>Display '
    html_file += b'this text in the browswer.</p>\n\n</body>\n</html>'

    valid_params_table = [
        [python_request, message + str(python_file)],
        [html_request, message + str(html_file)],
        [text_request, message + str(text_file)]]




    print (client('blah'))
    return valid_params_table
"""
    python_file = str(open('server.py', 'r').read().encode('utf8'))

    text_request = 'GET requestfiles/sample.txt HTTP/1.1\r\n'
    text_request += 'host: http://www.example.com\r\n\r\n'

    text_file = str(open('requestfiles/sample.txt', 'r').read().encode('utf8'))

    html_request = 'GET requestfiles/sample.html HTTP/1.1\r\n'
    html_request += 'host: http://www.example.com\r\n\r\n'

    html_file = str(open('requestfiles/sample.html', 'r').read().encode('utf8'))

    image_request = 'GET requestfiles/sample.py HTTP/1.1\r\n'
    image_request += 'host: http://www.example.com\r\n\r\n'

    image_file = str(open('requestfiles/images/russell.jpg',
                          'rb').read())

    valid_params_table = [
        [python_request, message + python_file],
        [html_request, message + html_file],
        [text_request, message + text_file]]
    return valid_params_table
"""


test_create_valid_params_table()