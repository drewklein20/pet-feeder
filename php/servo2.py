#!/usr/bin/env python

import time

import pigpio

pi = pigpio.pi() # Connect to local Pi.

#pi.set_servo_pulsewidth(17, 1000)
#time.sleep(0.5)
#pi.set_servo_pulsewidth(17, 1500)
#time.sleep(0.5)
pi.set_servo_pulsewidth(17, 2000)
time.sleep(5.5)
#pi.set_servo_pulsewidth(17, 1500)
#time.sleep(0.5)

# switch servo off
pi.set_servo_pulsewidth(17, 0);

pi.stop()
