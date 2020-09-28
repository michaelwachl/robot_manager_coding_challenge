Data: 27.09.2020  
Author: Michael Wachl  
Contact:  wachlm@web.de  
Project: Fleet Manager Coding Challenge

# Fleet Manager Coding Challenge

##Installation

Before starting, please install the dependencies using:
```
pip install -r requirements.txt
```

Hint: The project is developed with **python 3.5**

  
I used Anaconda and Pycharm to program and run this challenge. My python version is 3.5

##Structure and Functionality
My solution consits of 3 files:

**mqtt_client.py:** Class for MQTTClient creation, subscribes to robot topic and provides callback functions for
connection state and received message. Tries to connect to the broker. I used "mqtt.eclipse.org" as a broker. 

**robot.py:** Simulates robot fleet and publishes states. Uses mqtt_client.py

**database.py:** Provides a class for sqlite3 (SQLite) database manipulation. E.g. creation, inserting, fetching. 

**server.py:** This is the backend, where the FleetListener class uses the classes from database.py and mqtt_client.py 
to create a sqlite database for the robot stats at the beginning, if the database does not exists. It listens then to 
the robot states and inserts each message to the database. This class also dispatches the current message of the robot
to all websocket clients via asynchronous ioloop of the tornado server. 
MainHandler class fetches database and renders database.html for each new websocket request. 

**database.html:** This is the frontend of this project. It has the tasked to create new websocket for a browser 
request and creats a table of the robot states. It displays the database passed from the MainHandler and inserts each
message from the FleetListener. 

The two files in the class_templates folder are not used, but can be used for templates for future projects. 

##How to run
Use Pycharm or local machine and run the robot.py and server.py scripts


For local machine, change into the fleet_manager_coding_challenge and run both in two shells:

```
python3 server.py `
```
and 
```
python3 robot.py `
```

Once the server runs, you can open a websocket in the browser like Firefox with the address:
```
localhost:8888
```
Now you should see a table with the old and incoming robot messages. 

With Pycharm simply run both scripts and open browser with localhost:8888. 

See file **browser-ui.png** for expected result


