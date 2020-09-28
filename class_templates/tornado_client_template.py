from mqtt_client import MQTTClient
from tornado import escape
from tornado.ioloop import IOLoop, PeriodicCallback
import json
from tornado.websocket import websocket_connect
from tornado import gen
from tornado import ioloop

DEFAULT_CONNECT_TIMEOUT = 60
DEFAULT_REQUEST_TIMEOUT = 60

"""
Data: 27.09.2020  
Author: Michael Wachl  
Contact:  wachlm@web.de  
Project: Fleet Manager Coding Challenge
"""


class TornadoClient():
    """A simple class for the Robo Fleet Backend
    """
    def __init__(self):
        self.client = MQTTClient()

        # Messages from robots
        self.client.client.on_message = self.robot_message_received

        # Websocket
        self.url = "ws://localhost:8888/websocket"
        self.connect_timeout = DEFAULT_CONNECT_TIMEOUT
        self.request_timeout = DEFAULT_REQUEST_TIMEOUT
        self.ws_conn = None
        self.ws_connected = False
        self.connect_ws(self.url)

        PeriodicCallback(self.keep_alive, 20000).start()
        try:
            ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            self.close()


    def send_to_ws(self, data):
        """Send message to the server
        :param str data: message.
        """
        if self.ws_connected:
            print("trying to send")
            self.ws_conn.write_message(json.dumps(data))

    @gen.coroutine
    def connect_ws(self, url):
        """Connect to the server.
        :param str url: server URL.
        """
        try:
            print("trying to connect ws")
            self.ws_conn = yield websocket_connect(self.url)
        except Exception as e:
            print("connection error", e)
        else:
            self.ws_connected = True
            self.run()
            print("ws connected")

    def close(self):
        """Close connection.
        """
        if not self.ws_conn:
            raise RuntimeError('Web socket connection is already closed.')
        self.ws_connected = False
        self.ws_conn.close()

    @gen.coroutine
    def run(self):
        """needed for continuous communication
        """
        while True:
            msg = yield self.ws_conn.read_message()
            if msg is None:
                print("connection closed")
                self.ws_conn = None
                break

    def keep_alive(self):
        if self.ws_conn is None:
            self.ws_connected = False
            self.connect_ws(self.url)


if __name__ == "__main__":
    client = TornadoClient()