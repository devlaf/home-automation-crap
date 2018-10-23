##############################################
# dimmer.py
# 
# Controls a triac/zero-cross dimmer circuit
# via pwm.
##############################################

import threading
import wiringpi

AC_LOAD_PIN = 2
LEVEL_MAX = 100
LEVEL_MIN = 0

class Dimmer(object):
    
    def __init__(self):
        self._current_level = 0
        self._gpio_setup()
        self._listen()

    def __enter__(self):
        return self

    def __exit__(self):
        self._killall = True
        self.thread.join()
        wiringpi.softPwmWrite(AC_LOAD_PIN, LEVEL_MIN)


    def set_brightness(self, level):
        if level > LEVEL_MAX:
            self._current_level = LEVEL_MAX
        elif level < LEVEL_MIN:
            self._current_level = LEVEL_MIN
        else:
            self._current_level = level

    def get_brightness(self):
        return self._current_level
    
    def _gpio_setup(self):
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(AC_LOAD_PIN, 1)
        wiringpi.softPwmCreate(AC_LOAD_PIN, LEVEL_MIN, LEVEL_MAX)


    def _loop(self):
        while not self._killall:
            wiringpi.softPwmWrite(AC_LOAD_PIN, self._current_level)
            wiringpi.delay(20)

    def _listen(self):
        self._killall = False
        self.thread = threading.Thread(target=self._loop, args=())
        self.thread.daemon = True
        self.thread.start() 

