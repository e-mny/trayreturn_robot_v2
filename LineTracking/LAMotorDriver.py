# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 1000  # Min pulse length out of 4096
servo_max = 2000  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)
speed = 4095

print('Moving servo on channel 0, press Ctrl-C to quit...')
# State = 0 is short actuator
# State = 1 is long actuator
while True:
    # Direction = 0 is to lower actuator
    # Direction = 4095 is to raise actuator

    pwm.set_pwm(4, 0, 0) # Direction Linear Actuator
    pwm.set_pwm(5, 0, 2047) # Speed Linear Actuator
    time.sleep(2.5)
    pwm.set_pwm(4, 0, 0) # Direction Linear Actuator
    pwm.set_pwm(5, 0, 0) # Speed Linear Actuator
    time.sleep(2.5)
    pwm.set_pwm(4, 0, 4095) # Direction Linear Actuator
    pwm.set_pwm(5, 0, 2047) # Speed Linear Actuator
    time.sleep(5)


