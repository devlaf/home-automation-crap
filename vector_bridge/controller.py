#!/usr/bin/env python3

import sys
import os
import subprocess
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import anki_vector
sys.path.append(os.path.relpath("../config"))
from mqtt_topics import *
from mqtt_server import *

def setup_mqtt_client():
    mqtt_client.username_pw_set(mqtt_username, mqtt_password)
    mqtt_client.connect(mqtt_host, mqtt_port, 60)
    mqtt_client.on_connect = on_mqtt_connect
    mqtt_client.on_message = on_mqtt_message
    mqtt_client.loop_start()

def on_mqtt_connect(client, userdata, flags, rc):
    print("MQTT connected with status code " + str(rc))
    mqtt_subscribe(client, "blah_topic")

def on_mqtt_message(client, userdata, msg):
    print("Received message: [" + msg.topic + "] " + str(msg.payload))

    if msg.topic == "blah_topic"
        try:
            payload = int(msg.payload.decode("utf-8"))
        except ValueError:
            print("Invalid msg payload -- must be more integer-ish")
            dimmer.set_brightness(0)

def publish_mqtt(topic, payload):
    publish.single(topic=topic, payload=payload, hostname=mqtt_host,
        port=mqtt_port, auth={'username':mqtt_username, 'password':mqtt_password},
        keepalive=60, transport="tcp")

def mqtt_subscribe(client, topic):
    print("Subscribing to topic: " + topic)
    client.subscribe(topic)

def test(args):
    with anki_vector.Robot(args.serial) as robot:
        print("Say 'Hello World'...")
        robot.say_text("Hellooooooooooooo World")

def main():
    args = anki_vector.util.parse_command_args()
    test(args)

if __name__ == "__main__":
    main()
