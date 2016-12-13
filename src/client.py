"""Implementation of client."""

import socket
import sys


def client(message):
    """Create a client."""
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    try:
        client.connect(stream_info[-1])
        client.sendall(message.encode('utf8'))
        echo = echo_message(client, message)
    except (ConnectionRefusedError, KeyboardInterrupt):
        print ('Connection was not made or program was manually stopped')
        print ('Shutting down client')
        client.close()
        return None
    return echo


def echo_message(client, message):
    """Print and return the echoed message from the server."""
    buffer_length = 8
    message_complete = False
    output = ''
    while not message_complete:
        part = client.recv(buffer_length)
        output += part.decode('utf8')
        if len(part) < buffer_length:
            break
    print (output)
    return output


if __name__ == '__main__':
    client(sys.argv[1])
