import threading
import logging
import logging.config
import websocket
import json
import os
import sys
from queue import Queue


class MuggleClientThread(threading.Thread):
    def __init__(self, name, msgqueue):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger()
        self.name = name
        self.msgqueue = msgqueue
        self.ws = None

    def __del__(self):
        if self.ws is not None:
            self.ws.close()

    def run(self):
        self.logger.info("starting thread: %s %s" % (self.name, threading.current_thread()))
        sslopt_ca_certs = {'ca_certs': 'ca/server.crt', "check_hostname": False}
        self.ws = websocket.create_connection(
            "wss://150.109.44.64:5001/v1/ws",
            enable_multithread=True,
            sslopt=sslopt_ca_certs)

        self.msgqueue.put('ready', False)

        self.ws_recv()
        self.logger.info("exiting thread" + self.name)

    def ws_recv(self):
        while True:
            msg = self.ws.recv()
            msg = json.loads(msg)
            try:
                self.msgqueue.put(msg, False)
            except Queue.queue.Full:
                self.logger.warning('message queue is full')
            except:
                self.logger.error('unknown error in client')
                sys.exit(1)
