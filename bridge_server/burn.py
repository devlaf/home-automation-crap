#!/usr/bin/env python

import sys
import os
import asyncio
from multiprocessing import Process, Manager
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

sys.path.append(os.path.relpath("../config"))
from mqtt_topics import *
from mqtt_server import *

mqtt_client = mqtt.Client()

def mqtt_publish(topic, payload):
    publish.single(topic=topic, payload=payload, hostname=mqtt_host,
        port=mqtt_port, auth={'username':mqtt_username, 'password':mqtt_password},
        keepalive=60, transport="tcp")

def setup_mqtt_client():
    mqtt_client.username_pw_set(mqtt_username, mqtt_password)
    mqtt_client.connect(mqtt_host, mqtt_port, 60)
    mqtt_client.on_connect = on_mqtt_connect
    mqtt_client.on_message = on_mqtt_message
    mqtt_client.loop_start()

setup_mqtt_client()

