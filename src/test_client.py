"""Test the echo server functionality."""
# -*- coding: utf-8 -*-


def test_client():
    """Test client function using server in server.py."""
    from client import client
    assert client('short') == 'short'
    assert client('blah') == 'blah'
    assert client('88888888') == '88888888'
    assert client('±¥Ä') == '±¥Ä'

def test_response_ok():
     """Return a HTTP 200 response."""
    from server import test_response_ok
    message = 'HTTP/1.1 200 OK\nDate: '
    message += formatdate(timeval=None, localtime=False, usegmt=True)
    message += '\nThis is a minimal response\n'
    message.encode('utf8')
    assert message_ok() == message
     1. create one variable with whole message
     2,  then just do one assert that response_ok == message
 
 def test_response_error():
    from server import test_response_ok
    message = 'HTTP/1.1 200 OK\nDate: '
    message += formatdate(timeval=None, localtime=False, usegmt=True)
    message += '\nThis is a minimal response\n'
    message.encode('utf8')
    assert message_error() == message.encode('utf8')
   