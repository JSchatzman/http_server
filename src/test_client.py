"""Test the echo server functionality."""
# -*- coding: utf-8 -*-


def test_client():
    """Test client function using server in server.py."""
    from client import client
    assert client('short') == 'short'
    assert client('blah') == 'blah'
    assert client('88888888') == '88888888'
    assert client('±¥Ä') == '±¥Ä'
