import time
import board
import adafruit_hcsr04
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D1, echo_pin=board.D19)

# print(dir(sonar))
while True:
    # try:
    print((sonar.distance,))
    # except RuntimeError:
    #     print("Retrying!")
    #     pass
    # time.sleep(0.1)


1 2 3 4 6 5 7 9 13 37 
3 5 7 13 37
GPIO 2 3 4 27 26