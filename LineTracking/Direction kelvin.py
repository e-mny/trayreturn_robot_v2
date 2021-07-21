import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import Adafruit_PCA9685
from Status import Status

# Constants
speed = 250
timethreshold = 600 # 10 mins
weightthreshold = 4000

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
    # Kelvin: Middle two sensors white? Will there be a chance that this condition
    # is also satisfied when the robot is going straight? Perhaps detecting all 8
    # sensors black would be a better idea?
    return (matches_pattern('BBBBBBBB'))

def onTrack():
    # Kelvin: 2nd from middle white, and 1st from middle black?
    return (matches_pattern('**0BB0**'))

# Kelvin: left90 and leftsensor same pattern?
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
    
# Status:
# 0 = normal
# 1 = unload
# 2 = reload
# 3 = merge

def docking(): 
    # Main Station
    # Kelvin: Why is there two load pattern? 
    if loadpattern():
        if status == 1: # Unloading
            still()
            loweractuator()
            time.sleep(5)
            stopactuator()
            status = 2
        elif status == 2: # Loading
            still()
            increaseactuator()
            time.delay(5)
            stopactuator()
            status = 0
            return None
    elif leftsensor(): 
        left()
    elif rightsensor():
        right()
    else:
        straight()
        
def normal_tracking():
    if leftsensor(): 
        left()
    elif rightsensor():
        right()
    else:
        straight()
        

def sensorcheck():
    return ((weight.sensor > weightthreshold) or timer())

def movement(status):
    new_status = status

    # C1
    if isEndOfTrack():
        exit()

    # C2
    elif status == Status.NORMAL and left90() and sensorcheck():
        hardleft()
        new_status = Status.UNLOAD_SEQUENCE_STARTED

    # C3: K
    elif status == Status.UNLOAD_SEQUENCE_STARTED and matches_pattern('*****B**'):
        new_status = Status.WAITING_TO_UNLOAD
    
    # C4
    elif status == Status.WAITING_TO_UNLOAD and loadpattern():
        still()
        loweractuator()
        time.sleep(5)
        stopactuator()
        new_status = Status.WAITING_TO_LOAD

    # C5
    elif status == Status.WAITING_TO_LOAD and loadpattern():
        still()
        increaseactuator()
        time.delay(5)
        stopactuator()
        new_status = Status.WAITING_TO_MERGE

    # C6
    elif status == Status.WAITING_TO_MERGE and mergepattern():
        # Do stuff to merge
        new_status = Status.MERGING

    # C7
    elif status == Status.MERGING and right90():
        new_status = Status.NORMAL

    # D
    elif status != Status.UNLOAD_SEQUENCE_STARTED and status != Status.MERGING:
        normal_tracking()

    return new_status

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