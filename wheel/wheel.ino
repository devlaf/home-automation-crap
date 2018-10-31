#include <stdlib.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <AccelStepper.h>
#include "config/mqtt_server.h"
#include "esp8266_utils/serial_logger.h"
#include "esp8266_utils/wifi_tools.h"
#include "esp8266_utils/serial_logger.cpp"  // this arduino ide thing is annoying
#include "esp8266_utils/wifi_tools.cpp"

#define pin_button    1
#define pin_motor_enable   14
#define pin_motor_direction 5
#define pin_motor_step      4

const int num_positions = 8;
const int steps_per_position = 25;
const char* mqtt_spin_topic = "/wheel/spin";
const char* mqtt_spun_topic = "/wheel/spun";

long reset_opportunity = 0;

WiFiClient wifi_client;
PubSubClient mqtt_client;
AccelStepper stepper(1, pin_motor_step, pin_motor_direction);

void setup()
{
  pinMode(pin_button,          INPUT);
  pinMode(pin_motor_enable,    OUTPUT);
  pinMode(pin_motor_direction, OUTPUT);
  pinMode(pin_motor_step,      OUTPUT);
  setup_for_digital_dip();

  digitalWrite(pin_motor_enable, LOW);

  stepper.setMaxSpeed(1000);
  stepper.setSpeed(800);
  stepper.setAcceleration(500);

  setup_wifi();

  while(!ensure_mqtt_connection()) {
    delay(5000);
  }

  attachInterrupt(digitalPinToInterrupt(pin_button), spin, RISING);

  delay(2000);  // Yeah, you pulled-down an essential boot pin and were too lazy
                // to fix it, dummy. Don't drink and solder, kids.

  spin();
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
    mqtt_client.subscribe(mqtt_spin_topic);
    return true;
  }
  
  log_info("connection failed, status = %d", mqtt_client.state());
  return false;
}

void on_mqtt_msg(char* topic, byte* payload, unsigned int len)
{
  if (strcmp(topic, mqtt_spin_topic) != 0)
    return;

  spin();
}

int calculate_steps(int current, int target_pos, int extra_rotations)
{
  int full_rotation_steps = (num_positions * steps_per_position);
  int extra_rotation_adjustment = full_rotation_steps * extra_rotations;
  int zeroed_adjustment = full_rotation_steps - (current % full_rotation_steps);
  int target_adjustment = target_pos * steps_per_position;
  
  return current + extra_rotation_adjustment + zeroed_adjustment + target_adjustment;
}

void go_to_position_relative(int target_position, int extra_rotations)
{
  if (target_position < 0 || target_position > num_positions - 1) {
    log_info("Invalid posiiton [%d]. Must be between 0 and %s", target_position, num_positions);
    return;
  }

  int total_steps = calculate_steps(stepper.currentPosition(), target_position, extra_rotations);
  
  go_to_position_absolute(total_steps);
}

void go_to_position_absolute(int step)
{
  digitalWrite(pin_motor_enable, HIGH);
  
  stepper.moveTo(step);

  while (stepper.distanceToGo() != 0) {
    delay(10);
    stepper.run();
  }

  digitalWrite(pin_motor_enable, LOW);
}

void spin()
{
  log_info("spinning...");
  reset_opportunity = 0;

  int position = random(0, num_positions);
  int extra_spin = random(1,3);
  
  go_to_position_relative(position, extra_spin);

  size_t len = snprintf(NULL, 0, "%d", position);
  char* to_publish = (char*)malloc(len+1);
  sprintf(to_publish, "%d", position);
  
  mqtt_client.publish(mqtt_spun_topic, to_publish, true);
  free(to_publish);

  log_info("spun to position %d", position);
}

void loop()
{
  ensure_mqtt_connection();
  mqtt_client.loop();

  int button_state = digitalRead(pin_button);

  if (button_state == HIGH)
    spin();
}
