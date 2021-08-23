from Direction import left
from os import P_WAIT
import time
import board
import adafruit_hcsr04
import RPi.GPIO as GPIO

# Constants in cm
proximity = 60

rightsonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D15, echo_pin=board.D14)
backsonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D27, echo_pin=board.D17)
leftsonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D19, echo_pin=board.D13)
frontsonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D16, echo_pin=board.D26)


def tooClose(threshold=proximity):
    sensors = [frontsonar, backsonar, leftsonar, rightsonar]
    for i, sensor in enumerate(sensors):
        done_reading = False
        while not done_reading:
            # print(i)    
            try:
                if sensor.distance < proximity:
                    print(sensor.distance)
                    return True
                else:
                    done_reading = True
            except RuntimeError:
                pass

    return False

# def tooClose():
#     #  or (rightsonar.distance < proximity)
#     if ((frontsonar.distance < proximity) or (backsonar.distance < proximity) or (leftsonar.distance < proximity)):
#         return True # Something too close to robot
#     else:
#         return False # Continue moving



# try: 
while True:
    try:
        print("F: ", round(frontsonar.distance, 5))
        print("B: ", round(backsonar.distance, 5))
        print("L: ", round(leftsonar.distance, 5))
        print("R: ", round(rightsonar.distance, 5))
        

    except RuntimeError:
        print("Retrying!")
        
        pass

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("KeyboardInterrupt")
        quit()

    
    print("-----------------------")
    time.sleep(1)



# except KeyboardInterrupt:
#         GPIO.cleanup()
#         print("Keyboard Interrupt")
#         quit()


