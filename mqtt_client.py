import paho.mqtt.client as mqtt
import time

"""
Data: 27.09.2020  
Author: Michael Wachl  
Contact:  wachlm@web.de  
Project: Fleet Manager Coding Challenge
"""

class MQTTClient():
    """A simple class for mqqt clients
        """
    def __init__(self):
        self.client = mqtt.Client()
        self.client.connected_flag = False
        # self.broker = 'test.mosquitto.org'
        self.broker = "mqtt.eclipse.org"
        print("connecting to broker")
        self.client.connect(self.broker, 1883, 60)
        self.client.subscribe("knx/fleet_manager/robot_state")
        # bind callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

        # start loop for callbacks
        self.client.loop_start()

        while not self.client.connected_flag:
            print("Waiting for connection to ", self.broker)
            time.sleep(1)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.client.connected_flag = True
            print("Client connected")
        else:
            print("Bad connection with returned code: ", rc)

    def on_disconnect(self, client, userdata, flags, rc):
        self.client.connected_flag = False
        print("Client disconnected with returned code: ", rc)

    def on_message(self, client, userdata, msg):
        print("Message received-> " + msg.topic + " " + str(msg.payload))

    def on_publish(self, client, userdata, result):
        print("Data published")