#!/bin/bash

for i in {0..255}
do
mosquitto_pub -t '/power/sunlight/set' -u 'devin' -P 'nuts' -m "$i"
sleep 5000
done
