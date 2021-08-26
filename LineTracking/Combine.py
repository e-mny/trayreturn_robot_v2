import RPi.GPIO as GPIO
import Direction
from Direction import movement, debug, still, setup
from Status import Status
import ProximitySensor
from ProximitySensor import tooClose
import time
from WeightSensorExample import hx


status = Status.NORMAL
try:
    time.sleep(1) # 1s delay before it starts 
    while (True): 
        if tooClose():
                still()
                print("Someone is nearby")
                
                time.sleep(2) # Delay 3s until it checks surroundings again
        else:
            if __name__ == "__main__":
                x = 0
                t = 300
                debug()
                status = movement(status)
                # print("Average: ", round(hx.read_average()))
        

except KeyboardInterrupt:
    print("KeyboardInterrupt")
    still()

finally:
    GPIO.cleanup()
    print("\nCleaning up!!")
    print("Current Status: ", status)
    quit()

            

