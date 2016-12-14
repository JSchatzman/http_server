"""Implementation of client."""

import socket
import sys



def client(message):
    """Create a client."""
    infos = socket.getaddrinfo('127.0.0.1', 5038)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    eight_mult = False
    try:
        client.connect(stream_info[-1])
        if len(message) % 8 == 0:
            message = message + '-'
            eight_mult = True
        client.sendall(message.encode('utf8'))
        echo = echo_message(client, message, eight_mult)
    except (KeyboardInterrupt):
        print ('Connection was not made or program was manually stopped')
        print ('Shutting down client')
        client.close()
        return
    return echo


def echo_message(client, message, eight_mult):
    """Print and return the echoed message from the server."""
    buffer_length = 8
    message_complete = False
    output = ''
    while not message_complete:
        part = client.recv(buffer_length)
        output += part.decode('utf8')
        if len(part) < buffer_length or not part:
            break
    if eight_mult:
        print (output[:-1])
        return output[:-1]
    else:
        print (output)
        return output


if __name__ == '__main__':
    client('hell00ooooo')
