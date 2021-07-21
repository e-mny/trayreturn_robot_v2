import board
from adafruit_hcsr04 import HCSR04
with HCSR04(trigger_pin=board.D5, echo_pin=board.D6) as sonar:
    try:
        while True:
            print(sonar.distance)
            sleep(2)
    except KeyboardInterrupt:
        pass
