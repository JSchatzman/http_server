"""Implementation of server."""

import socket
from email.utils import formatdate


def server(http_response=False, buffer_length=8):
    """Create a server."""
    address = ('127.0.0.1', 5021)
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    server.bind(address)
    server.listen(1)
    try:
        while True:
            conn, addr = server.accept()
            message = message_handle(conn, buffer_length, http_response)
            conn.sendall(message.encode('utf8'))
    except (KeyboardInterrupt):
        print ('Shutting Down')
        server.close()


def message_handle(message, buffer_length, http_response=False):
    """Handle input message relative to buffer length."""
    message_complete = False
    output = ''
    while not message_complete:
        part = message.recv(buffer_length)
        output += part.decode('utf8')
        if len(part) < buffer_length or not part:
            message_complete = True
    if http_response:
        response = response_ok()
        return response
    else:
        response = output
    if output[-10:] == 'REMOVETHIS':
        print (output[:-10])
        return output
    else:
        print (output)
        return output


def response_ok():
    """Return a HTTP 200 response."""
    message = 'HTTP/1.1 200 OK\r\nDate: '
    message += formatdate(timeval=None, localtime=False, usegmt=True)
    message += '\r\nThis is a minimal response\r\n'
    message.encode('utf8')
    return message


def response_error():
    """Return a 500 error."""
    return '500 Internal Server Error'


if __name__ == '__main__':
    server(False)
