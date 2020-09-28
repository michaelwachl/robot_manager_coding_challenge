import json
import random
import time

from mqtt_client import MQTTClient


class RobotSimulator:
    def __init__(self):
        self.client = MQTTClient()
        while True:
            self.client.client.publish("knx/fleet_manager/robot_state",
                                       json.dumps({'position': {'x': random.randint(0, 10), 'y': random.randint(0, 10)},
                                                   'vehicle_id': 'AMR{}'.format(random.randint(0, 10)), 'driving': True,
                                                   'battery': 95.4, 'abort': False, 'order_id': None}))
            time.sleep(1)


if __name__ == "__main__":
    simu = RobotSimulator()