"""Implementation of server."""

import socket
from email.utils import formatdate


def server(http_response=False, buffer_length=8):
    """Create a server."""
    address = ('127.0.0.1', 5024)
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    server.bind(address)
    server.listen(1)
    try:
        while True:
            conn, addr = server.accept()
            message = message_handle(conn, buffer_length, True)
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
        error_message = parse_request(output)
        if error_message:
            print ('Error')
            return response_error(error_message)
        else:
            return response_ok()
    if output[-10:] == 'REMOVETHIS':
        print (output[:-10])
        return output
    else:
        print (output)
        return output


def parse_request(request):
    """Read client request and determine if it's valid."""
    try:
        error = ''
        header_lines = request.split('\r\n')
        print (header_lines)
        top_line = header_lines[0].split(' ')

        # Check validity of top line.

        if len(header_lines) < 3:
            error = 'This HTTP request is malformed.'
            raise ValueError
        elif top_line[0] != 'GET':
            error = 'HTTP request must be a GET'
            raise ValueError
        elif top_line[2] != 'HTTP/1.1':
            error = 'Must be HTTP version 1.1'
            raise ValueError
        host_line = [line for line in header_lines if line[:6] == 'host: ']

        # Check validitiy of host.

        if not host_line:
            error = 'No Host Provided.'
            raise ValueError
        else:
            host_line_contents = str(host_line).split(' ')
            if host_line_contents[1][:10].lower() != 'http://www':
                error = 'Invalid Host'
                raise ValueError

        # Check for correct ending of request.
        if header_lines[-1] != '' or header_lines[-2] != '':
            error = 'HTTP request not properly ended'
            raise ValueError
    except ValueError:
        if not error:
            return 'This HTTP request is malformed'
        return error


def response_ok():
    """Return a HTTP 200 response."""
    message = 'HTTP/1.1 200 OK\r\nDate: '
    message += formatdate(timeval=None, localtime=False, usegmt=True)
    message += '\r\nThis is a minimal response\r\n'
    message.encode('utf8')
    return message


def response_error(error_message):
    """Return a 500 error."""
    error_return = '400 Bad Request\r\n'
    error_return += error_message + '\r\n\r\n'
    return error_return


if __name__ == '__main__':
    server(True)
