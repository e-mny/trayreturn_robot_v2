import time
import board
import adafruit_hcsr04
import RPi.GPIO as GPIO

# Constants
proximity = 55

frontsonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D1, echo_pin=board.D19)
backsonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D12, echo_pin=board.D20)
leftsonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D13, echo_pin=board.D26)
rightsonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D16, echo_pin=board.D21)

def tooClose():
    if ((frontsonar.distance < proximity) or (backsonar.distance < proximity) or (leftsonar.distance < proximity) or (rightsonar.distance < proximity)):
        return True # Something too close to robot
    else:
        return False # Continue moving


# try:
    print("F: ", round(frontsonar.distance, 5))
    print("B: ", round(backsonar.distance, 5))
    print("L: ", round(leftsonar.distance, 5))
    print("R: ", round(rightsonar.distance, 5))
    print("-----------------------")
#except RuntimeError:
    print("Retrying!")
#time.sleep(2)
