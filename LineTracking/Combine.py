import RPi.GPIO as GPIO
import Direction
from Direction import movement, debug, still
from Status import Status
import ProximitySensor
from ProximitySensor import tooClose
import time



try: 
    while True: 
        if __name__ == "__main__":
            x = 0
            Status = Status.NORMAL
            t = 300
            
            #if (tooClose() == True):
                #still()
                #print("Someone is nearby")
                #time.sleep(3) # Delay 3s until it checks surroundings again
                
            #else:
            debug()
            Status = movement(Status)
            print("Running")

except KeyboardInterrupt:
    print("KeyboardInterrupt")
    still()

finally:
    GPIO.cleanup()
    print("\nCleaning up!!")
    quit()

            

