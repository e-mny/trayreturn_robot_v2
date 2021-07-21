import Direction
from Direction import movement, debug, still
from Status import Status
import ProximitySensor
from ProximitySensor import tooClose
import time

if __name__ == "__main__":
    x = 0
    Status = Status.NORMAL

    while True:
        if (tooClose() != True):
            Status = movement(Status)
            
        else:
            still()
            time.sleep(3) # Delay 3s until it checks again

