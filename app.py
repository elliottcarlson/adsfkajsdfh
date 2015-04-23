#!/usr/bin/python

from EventSource import EventSource
from UserClient import UserClient
import time, sys, os

EVENT_SOURCE_PORT = 9090
USER_CLIENT_PORT = 9099

if __name__ == '__main__':

    event_source_server = EventSource(EVENT_SOURCE_PORT)
    user_client_server = UserClient(USER_CLIENT_PORT)

    while 1:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print "DEATH"
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
