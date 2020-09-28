from database import FleetDatabase
from mqtt_client import MQTTClient

import json

"""
Data: 27.09.2020  
Author: Michael Wachl  
Contact:  wachlm@web.de  
Project: Fleet Manager Coding Challenge
"""

DEFAULT_CONNECT_TIMEOUT = 60
DEFAULT_REQUEST_TIMEOUT = 60

class FleetListener():
    """A simple class for the Robo Fleet Backend
    """
    def __init__(self):
        self.client = MQTTClient()

        # Messages from robots
        self.client.client.on_message = self.robot_message_received

        # Load/ Create Database
        self.data_base = FleetDatabase()
        self.db_connection = self.data_base.create_connection('Fleet_SQLite_Database.db')
        self.data_base.create_table(self.db_connection, self.data_base.table_sql)


    # dispatch messages from robots
    def robot_message_received(self, client, userdata, msg):
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        entities = json.loads(m_decode)
        # save to database
        elements = (entities["position"]["x"], entities["position"]["y"], entities["vehicle_id"], entities["driving"],
                    entities["battery"], entities["abort"], entities["order_id"])

        self.data_base.insert_to_table(elements)


if __name__ == "__main__":
    simu = FleetListener()
