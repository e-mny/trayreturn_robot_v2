import Direction
from Direction import movement, debug, still
from Status import Status
import ProximitySensor
from ProximitySensor import tooClose
import time
from WeightSensor import HX711



if __name__ == "__main__":
    x = 0
    Status = Status.NORMAL
    t = 300
    while True:
        if (tooClose() == True):
            still()
            time.sleep(3) # Delay 3s until it checks surroundings again
        else:
            Status = movement(Status)
            

