import TCPServer
from QueueManager import QueueManager
import socket
from pprint import pprint

class EventSource(TCPServer.TCPServer):

    def __init__(self, port):

        super(EventSource, self).__init__(port, EventSourceHandler)


class EventSourceHandler(TCPServer.StreamRequestHandler):

    def handle(self):

        done = False

        while not done:
            try:
                done = self.processEvent()
            except socket.error, e:
                done = True


    def processEvent(self):

        try:
            event = Event(self.rfile.readline().strip())
        except UnknownEvent, e:
            # print "Unknown event received..."
            return
        except:
            return

        """
        if event.type == 'Follow':

            if event.to_id not in self.server.follows:
                self.server.follows[event.to_id] = []

            self.server.follows[event.to_id].append(event.from_id)

        elif event.type == 'Unfollow':

            if (event.to_id in self.server.follows and 
                event.from_id in self.server.follows[event.to_id]):
                self.server.follows[event.to_id].remove(event.from_id)

        elif event.type == 'Broadcast':

            event.notify = list(self.server.users.keys())

        elif event.type == 'Status':

            if event.from_id in self.server.follows:
                event.notify = self.server.follows[event.from_id]
        """
        QueueManager.addEvent(event)


class UnknownEvent(Exception):

    pass


class Event(object):

    events = {
        'F': 'Follow',
        'U': 'Unfollow',
        'B': 'Broadcast',
        'P': 'Private',
        'S': 'Status'
    }

    raw = None
    sequence = None
    type = None
    from_id = None
    to_id = None

    notify = []

    def __init__(self, event):

        data = event.split('|')

        if len(data) <= 1 or data[1] not in self.events:
            raise UnknownEvent()

        self.raw = event
        self.sequence = data[0]
        self.type = self.events[data[1]]

        method = getattr(Event, self.events[data[1]])
        method(self, *data[2:])


    def Follow(self, *args):

        self.from_id = args[0]
        self.to_id = args[1]

        self.notify = [ self.to_id ]


    def Unfollow(self, *args):

        self.from_id = args[0]
        self.to_id = args[1]


    def Broadcast(self, *args):

        pass


    def Private(self, *args):

        self.from_id = args[0]
        self.to_id = args[1]

        self.notify = [ self.to_id ]


    def Status(self, *args):

        self.from_id = args[0]

