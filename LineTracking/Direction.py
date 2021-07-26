import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import Adafruit_PCA9685
from Status import Status
from WeightSensor import read_average

# Constants
speed = 250
timethreshold = 600 # 10 mins
weightthreshold = 820 # 2 trays

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

def debug(): 
    values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
    # Print the ADC values.
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
    # Pause for half a second.
    time.sleep(0.5)


def left():
    pwm.set_pwm(0, 0, 0) # Direction L
    pwm.set_pwm(1, 0, 0) # Speed L
    pwm.set_pwm(2, 0, 0) # Direction R
    pwm.set_pwm(3, 0, speed) # Speed R

def hardleft():
    pwm.set_pwm(0, 0, 4095) # Direction L
    pwm.set_pwm(1, 0, 1000) # Speed L
    pwm.set_pwm(2, 0, 0) # Direction R
    pwm.set_pwm(3, 0, 1000) # Speed R

def right():
    pwm.set_pwm(0, 0, 0) # Direction L
    pwm.set_pwm(1, 0, speed) # Speed L
    pwm.set_pwm(2, 0, 0) # Direction R
    pwm.set_pwm(3, 0, 0) # Speed R

def hardright():
    pwm.set_pwm(0, 0, 0) # Direction L
    pwm.set_pwm(1, 0, 1000) # Speed L
    pwm.set_pwm(2, 0, 4095) # Direction R
    pwm.set_pwm(3, 0, 1000) # Speed R
    
def straight():
    pwm.set_pwm(0, 0, 0) # Direction L
    pwm.set_pwm(1, 0, speed) # Speed L
    pwm.set_pwm(2, 0, 0) # Direction R
    pwm.set_pwm(3, 0, speed) # Speed R

def still():
    pwm.set_pwm(0, 0, 0) # Direction L
    pwm.set_pwm(1, 0, 0) # Speed L
    pwm.set_pwm(2, 0, 0) # Direction R
    pwm.set_pwm(3, 0, 0) # Speed R

def isEndOfTrack():
    return (matches_pattern('00000000'))

def onTrack():
    return (matches_pattern('**0BB0**'))

def left90():
    return (matches_pattern('BBBBB000'))

def right90():
    return (matches_pattern('000BBBBB'))

def leftsensor():
    return (matches_pattern('**B*****'))

def rightsensor():
    return (matches_pattern('*****B**'))

def loadpattern():
    return (matches_pattern('BBB00BBB'))

def mergepattern():
    return (matches_pattern('BBBBBBBB'))
    
def timer():
    time.sleep(timethreshold)
    return True
        
# 7 is L, 0 is R
    
# Direction = 0 is to lengthen actuator
# Direction = 4095 is to lower actuator    

def loweractuator():
    pwm.set_pwm(4, 0, speed) # Speed Linear Actuator
    pwm.set_pwm(5, 0, 4095) # Direction Linear Actuator
    
def increaseactuator():
    pwm.set_pwm(4, 0, speed) # Speed Linear Actuator
    pwm.set_pwm(5, 0, 0) # Direction Linear Actuator
    
def stopactuator():
    pwm.set_pwm(4, 0, 0) # Speed Linear Actuator
    pwm.set_pwm(5, 0, 0) # Direction Linear Actuator
        
def normal_tracking():
    if leftsensor(): 
        left()
    elif rightsensor():
        right()
    else:
        straight()
        

def sensorcheck():
    return ((read_average > weightthreshold) or timer())

def movement(Status):
    new_Status = Status

    # C1
    if isEndOfTrack():
        exit()

    # C2
    elif Status == Status.NORMAL and left90() and sensorcheck():
        hardleft()
        new_Status = Status.UNLOAD_SEQUENCE_STARTED

    # C3: K
    elif Status == Status.UNLOAD_SEQUENCE_STARTED and matches_pattern('*****B**'):
        new_Status = Status.WAITING_TO_UNLOAD
    
    # C4
    elif Status == Status.WAITING_TO_UNLOAD and loadpattern():
        still()
        loweractuator()
        time.sleep(5)
        stopactuator()
        new_Status = Status.WAITING_TO_LOAD

    # C5
    elif Status == Status.WAITING_TO_LOAD and loadpattern():
        still()
        increaseactuator()
        time.delay(5)
        stopactuator()
        new_Status = Status.WAITING_TO_MERGE

    # C6
    elif Status == Status.WAITING_TO_MERGE and mergepattern():
        hardleft()
        new_Status = Status.MERGING

    # C7
    elif Status == Status.MERGING and right90():
        new_Status = Status.NORMAL

    # D
    elif Status != Status.UNLOAD_SEQUENCE_STARTED and Status != Status.MERGING:
        normal_tracking()

    return new_Status

def matches_pattern(pattern):
    # ========================================================
    # Returns true if pattern indicated is matched
    # B = Black, O = White, * = Anything (don't care)
    #
    # Examples:
    #    [*****BBB]: Left90 pattern
    #    [BBB*****]: Right90 pattern
    # 
    # Usage:
    #    if matches_pattern([*****BBB]):
    #        still()
    #        hardright()
    #        ...
    # ========================================================
    assert len(pattern) == 8, 'Patterns should have length of 8'

    for i, p in enumerate(pattern):
        if p == '*':
            continue
        elif (p == 'B' and (mcp.read_adc(i) < 600)):
            # If reading is white, return False because pattern does not match
            return False
        elif (p == 'O' and (mcp.read_adc(i) > 900)):
            return False

    return True