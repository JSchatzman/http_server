"""Implementation of server."""

import socket


def server():
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
            message = message_handle(conn)
            conn.sendall(message.encode('utf8'))

    except (KeyboardInterrupt, BrokenPipeError):
        print ('Shutting Down')
        server.close()
        server.shutdown(1)


def message_handle(message):
    """Handle input message relative to buffer length."""
    buffer_length = 8
    message_complete = False
    output = ''
    while not message_complete:
        part = message.recv(buffer_length)
        output += part.decode('utf8')
        if len(part) < buffer_length:
            break
    return output

if __name__ == '__main__':
    server()
