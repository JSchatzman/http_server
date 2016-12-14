"""Implementation of server."""

import socket
from email.utils import formatdate


def server():
    """Create a server."""
    address = ('127.0.0.1', 5038)
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    server.bind(address)
    server.listen(1)
    try:
        while True:
            conn, addr = server.accept()
            message = message_handle(conn, True)
            conn.sendall(message.encode('utf8'))

    except (KeyboardInterrupt, BrokenPipeError):
        print ('Shutting Down')
        server.close()


def message_handle(message, http_response):
    """Handle input message relative to buffer length."""
    buffer_length = 8
    message_complete = False
    output = ''
    while not message_complete:
        part = message.recv(buffer_length)
        output += part.decode('utf8')
        if len(part) < buffer_length or not part:
            message_complete = True
    if http_response:
        response = response_ok()
    if (len(output) - 1) % 8 == 0 and output[-1:] == '-':
        print (output[:-1])
    else:
        print (output)
    return response


def response_ok():
    """Return a HTTP 200 response."""
    message = 'HTTP/1.1 200 OK\nDate: '
    message += formatdate(timeval=None, localtime=False, usegmt=True)
    message += '\nThis is a minimal response\n'
    message.encode('utf8')
    return message


def response_error():
    """Return a 500 error."""
    return '500 Internal Server Error'


if __name__ == '__main__':
    server()
