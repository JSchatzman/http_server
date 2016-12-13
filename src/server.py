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
            message_handle(conn)
    except KeyboardInterrupt:
        print ('Shutting Down')
        server.close()


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
    print (output)
    

server()
