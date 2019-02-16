/*  MQTT controller for a triac & zero-cross 
 *  dimmer circuit.
 * 
 *  Topic: /power/sunlight/set,   Msg: int, 0 - 255
 *  Topic: /power/sunlight/query  Msg: “”
 *  Topic: /power/sunlight/status Msg: int, 0 - 255
 * 
 */

#include <stdlib.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "config/mqtt_server.h"
#include "esp8266_utils/include/serial_logger.h"
#include "esp8266_utils/include/wifi_tools.h"
#include "esp8266_utils/src/serial_logger.cpp"
#include "esp8266_utils/src/wifi_tools.cpp"

#define PIN_DIMMER_OUT 3

const char* mqtt_set_topic = "/power/sunlight/set";
const char* mqtt_query_topic = "/power/sunlight/query";
const char* mqtt_status_topic = "/power/sunlight/status";

unsigned int target;
WiFiClient wifi_client;
PubSubClient mqtt_client;

void setup()
{
  pinMode(PIN_DIMMER_OUT, OUTPUT);

  setup_wifi();

  while(!ensure_mqtt_connection()) {
    delay(5000);
  }

  set_target(1);
  set_target(0);
}

void loop() 
{
  ensure_mqtt_connection();
  mqtt_client.loop();
}

void set_target(int val) 
{
  if (val < 0)
    target = 0;
  else if (val > 255)
    target = 255;
  else 
    target = val;
    
  analogWrite(PIN_DIMMER_OUT, target);
}

bool ensure_mqtt_connection()
{
  if (mqtt_client.connected())
    return true;

  log_info("Connecting to MQTT server...");

  mqtt_client.setClient(wifi_client);
  mqtt_client.setServer(mqtt_server, mqtt_server_port);
  mqtt_client.setCallback(on_mqtt_msg);

  if (mqtt_client.connect(hostname, mqtt_user, mqtt_password)) {
    log_info("Connected to mqtt server.");
    mqtt_client.subscribe(mqtt_set_topic);
    mqtt_client.subscribe(mqtt_query_topic);
    return true;
  }
  
  log_info("connection failed, status = %d", mqtt_client.state());
  return false;
}

void on_mqtt_msg(char* topic, byte* payload, unsigned int len)
{ 
  if (strcmp(topic, mqtt_set_topic) == 0) {
    char msg[len];
    memcpy(msg, payload, len);
    set_target(atoi(msg));
  }

  if (strcmp(topic, mqtt_query_topic) == 0) {
    publish_status();
  }
}

void publish_status()
{
  size_t len = snprintf(NULL, 0, "%d", target);
  char* to_publish = (char*)malloc(len+1);
  sprintf(to_publish, "%d", target);
  mqtt_client.publish(mqtt_status_topic, to_publish, true);
  free(to_publish);
}
