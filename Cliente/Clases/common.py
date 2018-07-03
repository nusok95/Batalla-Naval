import asyncio
import websockets
import json
from PyQt5.QtWidgets import QMessageBox
import threading
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

PORT = 8862


class ServerThread(threading.Thread):
    def __init__(self, host="localhost", port=8000):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.localServer = SimpleXMLRPCServer((self.host, self.port), allow_none=True)

    def add_function(self, function):
        self.localServer.register_function(function, function.__name__)

    def run(self):
        self.localServer.serve_forever()
