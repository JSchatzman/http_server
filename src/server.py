"""Implementation of server."""

import socket
from email.utils import formatdate
import mimetypes
import os


def server(http_response=False, buffer_length=8):
    """Create a server."""
    address = ('127.0.0.1', 5000)
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
    if output[-10:] == 'REMOVETHIS':
        output = output[:-10]
    if http_response:
        output, error_status = parse_request(output)
        if error_status:
            message_output = response_error(output)
        else:
            resolve_uri(output)
            message_output = response_ok()
    else:
        message_output = output
    if len(message_output) % 8 == 0:
        message_output += 'REMOVETHIS'
    return message_output


def parse_request(request):
    """Read client request and determine if it's valid."""
    try:
        error = ''
        header_lines = request.split('\r\n')
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
            if host_line_contents[1][:11].lower() != 'http://www.':
                error = 'Invalid Host'
                raise ValueError

        # Check for correct ending of request.
        if header_lines[-1] != '' or header_lines[-2] != '':
            error = 'HTTP request not properly ended'
            raise ValueError
    except ValueError:
        if not error:
            return ('This HTTP request is malformed.', True)
        return (error, True)

    # If no errors, return URI

    return (top_line[1], False)


def resolve_uri(uri):
    """If input is file, return contents, if dir, return dir contents."""
    uri = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                       uri)
    print (uri)
    if os.path.isfile(uri):
        print ('Yes')
        print (mimetypes.guess_type(uri))
        if 'text' in mimetypes.guess_type(uri)[0]:
            file = open(uri, 'r')
            file_contents = file.read().encode('utf8')
            print(file_contents)
            file.close()


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
