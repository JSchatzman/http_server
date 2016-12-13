"""Implementation of client."""

import socket


def client(message):
    """Create a client."""
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    try:
        client.connect(stream_info[-1])
    except ConnectionRefusedError:
        client.sendall(message.encode('utf8'))
        print ('Connection Refused')
    return client




print (client('blah'))

"""
[(<AddressFamily.AF_INET: 2>, 
    <SocketKind.SOCK_STREAM: 1>, 
    6, ''
    , 
    ('127.0.0.1', 80))
   ,(<AddressFamily.AF_INET: 2>
    , <SocketKind.SOCK_DGRAM: 2>
    , 17
    , ''
    ,('127.0.0.1', 80))]
"""