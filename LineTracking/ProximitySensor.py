import time
import board
import adafruit_hcsr04
import RPi.GPIO as GPIO

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D1, echo_pin=board.D19)

while True:
    try:
        print(sonar.distance)
    except RuntimeError:
        print("Retrying!")
    time.sleep(2)
