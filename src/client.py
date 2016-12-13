"""Implementation of client."""

import socket


def client(message):
    """Create a client."""
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    try:
        client.connect(stream_info[-1])
        client.sendall(message.encode('utf8'))
    except ConnectionRefusedError:
        print ('Connection Refused')
    return client


client('8888888888888888')