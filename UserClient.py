import TCPServer
import socket


class UserClient(TCPServer.TCPServer):

    def __init__(self, port):

        super(UserClient, self).__init__(port, UserClientHandler)
        

class UserClientHandler(TCPServer.StreamRequestHandler):

    def handle(self):

        self.user_id = self.rfile.readline().strip()
        self.server.users[self.user_id] = self.wfile


#        print "Registering %s as client for %s" % (self.wfile, self.user_id)

        done = False

        while not done:
            try:
                pass
            except socket.error, e:
                done = True

    def finish(self):
        if self.server.users.get(self.user_id):
            del(self.server.users[self.user_id])

#        self.request(shutdown(2))
        self.request.close()

