import RPi.GPIO as GPIO
import Direction
from Direction import movement, debug, still
from Status import Status
import ProximitySensor
from ProximitySensor import tooClose
import time




status = Status.WAITING_TO_UNLOAD
try:
    time.sleep(1) # 1s delay before it starts 
    while True: 
        if __name__ == "__main__":
            x = 0
            t = 300
            
            # if tooClose():
            #     still()
            #     print("Someone is nearby")
            #     time.sleep(3) # Delay 3s until it checks surroundings again
                
            # else:
            debug()
            status = movement(status)
        

except KeyboardInterrupt:
    print("KeyboardInterrupt")
    still()

finally:
    GPIO.cleanup()
    print("\nCleaning up!!")
    quit()

            

