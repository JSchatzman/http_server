"""Allowing concurrent clients to interact with the server."""
from server import server


if __name__ == '__main__':
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    patch_all()
    server = StreamServer(('127.0.0.1', 5047), server)
    print ('Starting Concurrent Server')
    try:
        server.serve_forever()
    except(KeyboardInterrupt):
        print ('Shutting Down')
        server.close()
