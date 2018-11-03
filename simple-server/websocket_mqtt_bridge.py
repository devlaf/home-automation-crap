#!/usr/bin/env python

import sys
import os
import asyncio
import websockets
from multiprocessing import Process, Manager
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

sys.path.append(os.path.relpath("../config"))
from mqtt_topics import *
from mqtt_server import *

websocket_port = 8765
mqtt_client = mqtt.Client()
connected_ws_clients = set()
manager = Manager()
messages = manager.list()

async def on_websocket_connection(websocket, path):
    connected_ws_clients.add(websocket)

    async for message in websocket:
        if message == "spin":
            mqtt_publish(wheel_spin, "")

def websocket_publish(msg):
    messages.append(msg)

async def publish_timer():
    while True:
        to_remove = set()
        for ws in connected_ws_clients:
            try:
                for msg in messages:
                    await ws.send(msg)
            except:
                to_remove.add(ws)
        for removable in to_remove:
            connected_ws_clients.remove(removable)
        del messages[:]

        await asyncio.sleep(1)

def on_mqtt_message(client, userdata, msg):
    print("Received message: [" + msg.topic + "] " + str(msg.payload))

    if msg.topic == wheel_spun:
        websocket_publish("spun")

def mqtt_publish(topic, payload):
    publish.single(topic=topic, payload=payload, hostname=mqtt_host,
        port=mqtt_port, auth={'username':mqtt_username, 'password':mqtt_password},
        keepalive=60, transport="tcp")

def on_mqtt_connect(client, userdata, flags, rc):
    print("MQTT connected with status code " + str(rc))
    mqtt_subscribe(client, wheel_spin)
    mqtt_subscribe(client, wheel_spun)

def mqtt_subscribe(client, topic):
    print("Subscribing to topic: " + topic)
    client.subscribe(topic)

def setup_mqtt_client():
    mqtt_client.username_pw_set(mqtt_username, mqtt_password)
    mqtt_client.connect(mqtt_host, mqtt_port, 60)
    mqtt_client.on_connect = on_mqtt_connect
    mqtt_client.on_message = on_mqtt_message
    mqtt_client.loop_start()


setup_mqtt_client()
tasks = [websockets.serve(on_websocket_connection, '', websocket_port), publish_timer()]
asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
asyncio.get_event_loop().run_forever()

