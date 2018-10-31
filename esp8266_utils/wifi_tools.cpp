#include <stdlib.h>
#include <ESP8266WiFi.h>
#include "serial_logger.h"

#define pin_net_id_bit_3 12
#define pin_net_id_bit_2 13
#define pin_net_id_bit_1 15
#define pin_net_id_bit_0 3

char* hostname;

void setup_for_digital_dip()
{
  pinMode(pin_net_id_bit_3, INPUT);
  pinMode(pin_net_id_bit_2, INPUT);
  pinMode(pin_net_id_bit_1, INPUT);
  pinMode(pin_net_id_bit_0, INPUT);
}

int read_dip_id_digital()
{
  int bit_3 = digitalRead(pin_net_id_bit_3);
  int bit_2 = digitalRead(pin_net_id_bit_2);
  int bit_1 = digitalRead(pin_net_id_bit_1);
  int bit_0 = digitalRead(pin_net_id_bit_0);

  return (8 * bit_3) + (4 * bit_2) + (2 * bit_1) + bit_0;
}

void setup_for_analog_dip(int pin_analog_read)
{
  pinMode(pin_analog_read, INPUT);
}

int read_dip_id_analog(int pin_analog_read)
{
  return (analogRead(pin_analog_read) / 10);
}

int read_dip_id() 
{
  return read_dip_id_digital();
}

void set_hostname()
{
  int id = read_dip_id();

  size_t len = snprintf(NULL, 0, "esp8266-%d", id);
  hostname = (char*)malloc(len+1);
  sprintf(hostname, "esp8266-%d", id);

  log_info("Setting host name to %s", hostname);

  WiFi.hostname(hostname);
}

void setup_wifi()
{
  set_hostname();

  log_info("Connecting to %s", wifi_ssid);

  WiFi.begin(wifi_ssid, wifi_password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    log_info("*");
  }

  log_info("WiFi connected at IP Address: %s", WiFi.localIP().toString().c_str(),3,0);
}
