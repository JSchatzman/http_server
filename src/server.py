"""Implementation of server."""

import socket
from email.utils import formatdate
import mimetypes
import os


def server(http_response=False, buffer_length=8):
    """Create a server."""
    address = ('127.0.0.1', 5047)
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
            request_resonse = resolve_uri(output)
            if request_resonse:
                message_output = response_ok(request_resonse)
            else:
                message_output = response_error(404)
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
            error = 400
            raise ValueError
        elif top_line[0] != 'GET':
            error = 405
            raise ValueError
        elif top_line[2] != 'HTTP/1.1':
            error = 505
            raise ValueError
        host_line = [line for line in header_lines if line[:6] == 'host: ']

        # Check validity of host.

        if not host_line:
            error = '400 no host'
            raise ValueError
        else:
            host_line_contents = str(host_line).split(' ')
            if host_line_contents[1][:11].lower() != 'http://www.':
                error = '400 invalid host'
                raise ValueError

        # Check for correct ending of request.

        if header_lines[-1] != '' or header_lines[-2] != '':
            error = '400 bad ending'
            raise ValueError
    except ValueError:
        if not error:
            return (400, True)
        return (error, True)

    # If no errors, return URI.

    return (top_line[1], False)


def resolve_uri(uri):
    """If input is file, return contents, if dir, return dir contents."""
    uri = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                       uri)

    # Return URI if file.

    if os.path.isfile(uri):
        if 'text' in mimetypes.guess_type(uri)[0]:
            file = open(uri, 'r')
            contents = file.read().encode('utf8')
            print(contents)
        else:
            file = open(uri, 'rb')
            contents = file.read()
            print(contents)
        file.close()
        return contents

    # Return HTML listing if URI is directory.

    elif os.path.isdir(uri):
        contents = ['<!DOCTYPE html>', '<html><body>']
        for item in os.listdir(uri):
            contents.append('<a href="' + item + '">')
        contents.extend(['</body>', '</html>'])
        return ''.join(contents)


def response_ok(uri_result=None):
    """Return a HTTP 200 response."""
    message = 'HTTP/1.1 200 OK\r\nDate: '
    message += formatdate(timeval=None, localtime=False, usegmt=True)
    message += '\r\n\r\n'
    if uri_result:
        message += str(uri_result) + '\r\n\r\n'
    message.encode('utf8')
    return message


def response_error(error_code):
    """Return a 400 error."""
    if error_code == 405:
        error_return = '405 Method Not Allowed\r\n'
        error_return += 'Must be a GET method'
    elif error_code == 505:
        error_return = '505 HTTP Version Not Supported\r\n'
        error_return += 'Must be using HTTP v1.1'
    elif error_code == 404:
        error_return = '404 Not Found\r\n'
        error_return += 'The Requested URI Could Not Be Found'
    elif error_code == '400 no host':
        error_return = '400 Bad Request\r\n'
        error_return += 'No host was provided'
    elif error_code == '400 invalid host':
        error_return = '400 Bad Request\r\n'
        error_return += 'Invalid Host Provied'
    elif error_code == '400 bad ending':
        error_return = '400 Bad Request\r\n'
        error_return += 'Improperly Ended Request'
    else:
        error_return = '400 Bad Request\r\n'
        error_return += 'Malformed Request'
    error_return.encode('utf8')
    return error_return


if __name__ == '__main__':
    server(True)
