from TCPServer import ThreadedTCPServer
from pprint import pprint

class Queue(object):

    events = {}


class QueueManager(Queue):

    last_sent = 0

    @staticmethod
    def addEvent(event):

        Queue.events[event.sequence] = event

        QueueManager.parseQueue()


    @staticmethod
    def parseQueue():

        done = False

        while not done:

            if str(QueueManager.last_sent + 1) in Queue.events:

                QueueManager.last_sent += 1

                event = QueueManager.handleQueuedEvent(Queue.events[str(QueueManager.last_sent)])

                QueueManager.sendEvent(Queue.events[str(QueueManager.last_sent)])

                del(Queue.events[str(QueueManager.last_sent)])

            else:

                done = True


    @staticmethod
    def handleQueuedEvent(event):

        if event.type == 'Follow':

            if event.to_id not in ThreadedTCPServer.follows:
                ThreadedTCPServer.follows[event.to_id] = []

            ThreadedTCPServer.follows[event.to_id].append(event.from_id)

        elif event.type == 'Unfollow':

            if (event.to_id in ThreadedTCPServer.follows and
                event.from_id in ThreadedTCPServer.follows[event.to_id]):
                ThreadedTCPServer.follows[event.to_id].remove(event.from_id)

        elif event.type == 'Broadcast':

            event.notify = list(ThreadedTCPServer.users.keys())

        elif event.type == 'Status':

            if event.from_id in ThreadedTCPServer.follows:
                event.notify = ThreadedTCPServer.follows[event.from_id]

        return event

    @staticmethod
    def sendEvent(event):

        if not event.notify:
            return

        for user in event.notify:

            if user in ThreadedTCPServer.users.keys():

                print "Sending \"%s\" to user id %s   (s: %s, t: %s)" % (event.raw, user, event.sequence, event.type)

                ThreadedTCPServer.users[user].write(event.raw + "\r\n")

