import threading
import SocketServer


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    users = {}
    follows = {}

class BaseRequestHandler(SocketServer.BaseRequestHandler):
    pass


class StreamRequestHandler(SocketServer.StreamRequestHandler):
    pass


class TCPServer(object):

    server = False
    thread = False

    def __init__(self, port, handler):

        SocketServer.ThreadingTCPServer.allow_reuse_address = True

        self.server = ThreadedTCPServer(('', port), handler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.setDaemon(True)
        self.thread.start()
