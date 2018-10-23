import sys
import os
import subprocess
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from dimmer import Dimmer
sys.path.append(os.path.relpath("../config"))
from mqtt_topics import *
from mqtt_server import *

dimmer = Dimmer()
mqtt_client = mqtt.Client()

def setup_mqtt_client():
    mqtt_client.username_pw_set(mqtt_username, mqtt_password)
    mqtt_client.connect(mqtt_host, mqtt_port, 60)
    mqtt_client.on_connect = on_mqtt_connect
    mqtt_client.on_message = on_mqtt_message
    mqtt_client.loop_start()

def on_mqtt_connect(client, userdata, flags, rc):
    print("MQTT connected with status code " + str(rc))
    mqtt_subscribe(client, sunlight_lamp_set)
    mqtt_subscribe(client, sunlight_lamp_query)

def on_mqtt_message(client, userdata, msg):
    print("Received message: [" + msg.topic + "] " + str(msg.payload))

    if msg.topic == sunlight_lamp_set:
        try:
            payload = int(msg.payload.decode("utf-8"))
            dimmer.set_brightness(payload)
        except ValueError:
            print("Invalid msg payload -- must be more integer-ish")
            dimmer.set_brightness(0)

    if msg.topic == sunlight_lamp_query:
        publish_mqtt(sunlight_lamp_status, dimmer.get_brightness())

def publish_mqtt(topic, payload):
    publish.single(topic=topic, payload=payload, hostname=mqtt_host,
        port=mqtt_port, auth={'username':mqtt_username, 'password':mqtt_password},
        keepalive=60, transport="tcp")

def mqtt_subscribe(client, topic):
    print("Subscribing to topic: " + topic)
    client.subscribe(topic)


dimmer = Dimmer()
setup_mqtt_client()

mqtt_client.loop_forever()

