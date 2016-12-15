"""Implementation of client."""

import socket
import sys


def client(message, buffer_length=8):
    """Create a client."""
    infos = socket.getaddrinfo('127.0.0.1', 5050)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    try:
        client.connect(stream_info[-1])
        if len(message) % buffer_length == 0:
            message += 'REMOVETHIS'
        client.sendall(message.encode('utf8'))
        echo = echo_message(client, message, buffer_length)
    except (KeyboardInterrupt):
        print ('Connection was not made or program was manually stopped')
        print ('Shutting down client')
        client.close()
        return
    return echo


def echo_message(client, message, buffer_length):
    """Print and return the echoed message from the server."""
    message_complete = False
    output = ''
    while not message_complete:
        part = client.recv(buffer_length)
        output += part.decode('utf8')
        if len(part) < buffer_length or not part:
            break
    if output[:-10] == 'REMOVETHIS':
        print(output[:-10])
        return output[:-10]
    else:
        print(output)
        return output


if __name__ == '__main__':
    client(sys.argv[1])
