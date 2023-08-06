import json
from socket import socket
from threading import Thread, Event

from notify_cli.binary_protocol import BinaryProtocol


class NotifyClient:
    def __init__(self, host, port):
        sock = socket()
        sock.connect((host, port))
        self.client = BinaryProtocol(sock)
        self.subscribers = {}
        self.thread = None
        self.connection_lost_event = Event()

    def _run(self):
        try:
            while True:
                event = json.loads(self.client.receive().decode())
                for callback in self.subscribers.get(event['event'], []):
                    callback(event)
        except ConnectionError:
            self.thread = None
            self.connection_lost_event.set()

    def subscribe(self, event, callback):
        if not self.thread:
            self.thread = Thread(target=self._run, daemon=True)
            self.thread.start()
        if event not in self.subscribers:
            self.client.send(json.dumps({
                'type': 'subscribe',
                'event': event
            }))
            self.subscribers[event] = []
        self.subscribers[event].append(callback)

    def unsubscribe(self, event, callback):
        self.subscribers[event].remove(callback)
        if not self.subscribers[event]:
            del self.subscribers[event]
            self.client.send(json.dumps({
                'type': 'unsubscribe',
                'event': event
            }))

    def send(self, event, data):
        self.client.send(json.dumps({
            'type': 'event',
            'event': event,
            'data': data
        }))
