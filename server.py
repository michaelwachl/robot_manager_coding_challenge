import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado import ioloop

from database import FleetDatabase
from mqtt_client import MQTTClient
import json

import asyncio

"""
Data: 27.09.2020  
Author: Michael Wachl  
Contact:  wachlm@web.de  
Project: Fleet Manager Coding Challenge

Check Database and Messages on localhost:8888 in browser
"""

clients = []

class FleetListener:
    """A simple class for the Robot Fleet Backend, receives messages from robots, saves it to database and sends it to
    all websocket clients.
    """
    def __init__(self):
        self.client = MQTTClient()
        # callback messages from robots
        self.client.client.on_message = self.robot_message_received

        # Load/ Create Database
        self.data_base = FleetDatabase()
        self.db_connection = self.data_base.create_connection('Fleet_SQLite_Database.db')
        self.data_base.create_table(self.db_connection, self.data_base.table_sql)

    def robot_message_received(self, client, userdata, msg):
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        entities = json.loads(m_decode)
        # save to database
        elements = (entities["position"]["x"], entities["position"]["y"], entities["vehicle_id"], entities["driving"],
                    entities["battery"], entities["abort"], entities["order_id"])

        self.data_base.insert_to_table(elements)
        print("Robot state received")
        # sent to websockets
        self.async_io_helper(entities)

    def broadcast(self, message):
        for ws in clients:
            if not ws.ws_connection.stream.socket:
                print("Web socket does not exist anymore")
                clients.remove(ws)
            else:
                try:
                    ws.write_message(message)
                    print("Send message to %s ws clients" % len(clients))
                except Exception as e:
                    print("Error: ", e)

    def async_io_helper(self, message):
        # use asyncio and multithreading together to broadcast messages to clients
        io_loop.asyncio_loop.call_soon_threadsafe(self.broadcast, message)


class MainHandler(tornado.web.RequestHandler):
    data_base = FleetDatabase()

    async def get(self):
        print("Loading database")
        # load database
        data_base = FleetDatabase()
        db_connection = data_base.create_connection(data_base.db_name)
        db_entities = data_base.fetch_columns(db_connection)
        # display database
        if db_entities:
            self.render("database.html", items=db_entities)
        else:
             #self.set_status(404)
             #self.write("Error: Database not found")
             self.render("database.html", items=[])


class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    connections = set()

    def check_origin(self, origin):
        return True

    def open(self):
        self.connections.add(self)
        clients.append(self)
        print(self)
        # self.write_message('connected!')
        print("WebSocket new client connected")

    def on_close(self):
        self.connections.remove(self)
        clients.remove(self)
        print("WebSocket client disconnected")

    def on_message(self, message):
        print("got message %r", message)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", SimpleWebSocket)
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)

    tornado.ioloop.IOLoop.configure("tornado.platform.asyncio.AsyncIOLoop")
    io_loop = tornado.ioloop.IOLoop.current()
    asyncio.set_event_loop(io_loop.asyncio_loop)

    # pass main loop to class
    listener = FleetListener()
    ioloop.IOLoop.current().start()


