"""Test the echo server functionality."""
# -*- coding: utf-8 -*-


def test_client():
    """Test client function using server in server.py."""
    from client import client
    assert client('short') == 'short'
    assert client('blah') == 'blah'
    assert client('88888888') == '88888888'
    # Not sure how to get non anscii characters to test in 2 and 3.
    # assert client('±¥Ä') == '±¥Ä'
