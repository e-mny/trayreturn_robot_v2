import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import Adafruit_PCA9685
from Status import Status
from WeightSensor import HX711
hx = HX711(6, 5, 128)

# Constants
speed = 1300
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
    #time.sleep(0.1)

speed_diff = int(.35 * speed)

def left(factor):
    pwm.set_pwm(0, 0, 0) # Direction L
    # pwm.set_pwm(1, 0, 0) # Speed L
    pwm.set_pwm(1, 0, speed - int(speed_diff * factor))
    pwm.set_pwm(2, 0, 0) # Direction R
    # pwm.set_pwm(3, 0, speed - 200) # Speed R
    pwm.set_pwm(3, 0, speed + int(speed_diff * factor))

def hardleft():
    pwm.set_pwm(0, 0, 4095) # Direction L
    pwm.set_pwm(1, 0, speed - 100) # Speed L
    pwm.set_pwm(2, 0, 0) # Direction R
    pwm.set_pwm(3, 0, speed - 100) # Speed R

def right(factor):
    pwm.set_pwm(0, 0, 0) # Direction L
    # pwm.set_pwm(1, 0, speed - 200) # Speed L
    pwm.set_pwm(1, 0, speed + int(speed_diff * factor))
    pwm.set_pwm(2, 0, 0) # Direction R
    # pwm.set_pwm(3, 0, 0) # Speed R
    pwm.set_pwm(3, 0, speed - int(speed_diff * factor))

def hardright():
    pwm.set_pwm(0, 0, 0) # Direction L
    pwm.set_pwm(1, 0, speed - 100) # Speed L
    pwm.set_pwm(2, 0, 4095) # Direction R
    pwm.set_pwm(3, 0, speed - 100) # Speed R
    
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
    return (matches_pattern('OOOOOOOO'))

def onTrack():
    return (matches_pattern('OO*BB*OO'))

def left90():
    return (matches_pattern('O**BBBBB'))

def right90():
    return (matches_pattern('BBBBB**O'))

def leftsensor():
    if matches_pattern('*****B**'):
        return 1
    elif matches_pattern('******B*'):
        return 1.5
    elif matches_pattern('*******B'):
        return 2
    else:
        return False
    # return (matches_pattern('******B*') or matches_pattern('*******B'))
    # return (matches_pattern('OOO*BB**'))

def rightsensor():
    if matches_pattern('*B******'):
        return 1
    elif matches_pattern('B*******'):
        return 1
    else:
        return False
    # return (matches_pattern('*B******') or matches_pattern('B*******'))
    # return (matches_pattern('**BB*OOO'))

def loadpattern():
    return (matches_pattern('BB*OO*BB'))

def mergepattern():
    return (matches_pattern('BBBBBBBB'))
    
def timer():
    time.sleep(timethreshold)
    return True
        
# 7 is L, 0 is R
    
# Direction = 0 is to lower actuator
# Direction = 4095 is to raise actuator    

def loweractuator():
    pwm.set_pwm(4, 0, 0) # Direction Linear Actuator
    pwm.set_pwm(5, 0, speed) # Speed Linear Actuator
    
def increaseactuator():
    pwm.set_pwm(4, 0, 4095) # Direction Linear Actuator
    pwm.set_pwm(5, 0, speed) # Speed Linear Actuator
    
def stopactuator():
    pwm.set_pwm(4, 0, 0) # Direction Linear Actuator
    pwm.set_pwm(5, 0, 0) # Speed Linear Actuator
        
def normal_tracking():
    rs = rightsensor()
    ls = leftsensor()
    if rs is not False:
        right(rs)
        print("right")
    elif ls is not False:
        left(ls)
        print("left")
    else:
        straight()
        print("straight")
        
    # if rightsensor(): 
    #     right()
    #     print("Right")
        
    # elif leftsensor():
    #     left()
    #     print("Left")
        
    # else:
    #     straight()
    #     print("Straight")
        

def sensorcheck():
    return True
    #((hx.read_average() > weightthreshold) or timer())

def movement(status):
    new_status = status

    # C1
    if status == Status.NORMAL and right90() and (sensorcheck() == False):
        print("C1")
        straight()
        time.sleep(1) # Change if change speed
        

    # C2
    if status == Status.NORMAL and right90() and (sensorcheck() == True):
        print("C2")
        straight()
        time.sleep(3) # Change if change speed
        hardright()
        time.sleep(2) # Change if change speed
        new_status = Status.UNLOAD_SEQUENCE_STARTED
        

    # C3: 
    elif status == Status.UNLOAD_SEQUENCE_STARTED:
        while not matches_pattern('*****B**'):
            hardright()
            print("C3")
        new_status = Status.WAITING_TO_UNLOAD
    
    # C4
    elif status == Status.WAITING_TO_UNLOAD:
        if loadpattern():
            print("C4")
            straight()
            time.sleep(0.5)
            still()
            loweractuator()
            time.sleep(12)
            # left()
            # time.sleep(0.5)
            
            new_status = Status.WAITING_TO_LOAD
        else:
            normal_tracking()
        

    # C5
    elif status == Status.WAITING_TO_LOAD:
        if loadpattern():
            print("C5")
            straight()
            time.sleep(0.5)
            still()
            increaseactuator()
            time.sleep(12)
            
    
            new_status = Status.WAITING_TO_MERGE
        else:
            normal_tracking()

    # C6
    elif status == Status.WAITING_TO_MERGE:
        if mergepattern():
            print("C6")
            straight()
            time.sleep(3) # Change if change speed
            hardright()
            time.sleep(2) # Change if change speed
            new_status = Status.MERGING
        else:
            normal_tracking()

    # C7
    elif status == Status.MERGING:
        while not matches_pattern('**B*****'):
            hardright()
            print("C7")
        new_status = Status.NORMAL

    # # D
    # elif isEndOfTrack() and status == Status.NORMAL:
    #     print("D")
    #     still()
    #     hardleft()
    #     #exit()

    # Else
    else: # Status != Status.UNLOAD_SEQUENCE_STARTED and status != Status.MERGING:
        print("Else")
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
        elif (p == 'B' and (mcp.read_adc(i) < 950)):
            # If reading is white, return False because pattern does not match
            return False
        elif (p == 'O' and (mcp.read_adc(i) > 950)):
            return False

    return True
