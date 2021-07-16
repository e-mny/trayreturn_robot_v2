import time
import status
status = 0

# Constants
speed = 250
timethreshold = 600 # 10 mins
weightthreshold = (weight of two trays)

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

x = 0

def isEndOfTrack():
    return ((mcp.read_adc(3) == 0) and (mcp.read_adc(4) == 0))

def onTrack():
    return ((mcp.read_adc(2) == 0) and (mcp.read_adc(5) == 0))

def left90():
    return ((mcp.read_adc(5) != 0) and (mcp.read_adc(6) != 0) and (mcp.read_adc(7) != 0))

def right90():
    return ((mcp.read_adc(0) != 0) and (mcp.read_adc(1) != 0) and (mcp.read_adc(2) != 0))

def leftsensor():
    return ((mcp.read_adc(5) != 0) or (mcp.read_adc(6) != 0) or (mcp.read_adc(7) != 0))

def rightsensor():
    return ((mcp.read_adc(0) != 0) or (mcp.read_adc(1) != 0) or (mcp.read_adc(2) != 0))

def loadpattern():
    return ((mcp.read_adc(0) != 0) and (mcp.read_adc(1) != 0) and (mcp.read_adc(2) != 0) and (mcp.read_adc(3) == 0) and (mcp.read_adc(4) == 0) and (mcp.read_adc(5) != 0) and (mcp.read_adc(6) != 0) and (mcp.read_adc(7) != 0))

def timer():
    time.sleep(timethreshold)
    return True

        
# 7 is L, 0 is R
# White colour: mcp.read_adc(x) = 0
# Black colour: mcp.read_adc(x) != 0

# Status:
# 0 = normal
# 1 = unload
# 2 = main station
# 3 = reload
# 4 = merge
    
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

def docking():

    # Main Station
    if loadpattern():
        still()
        loweractuator()
        time.sleep(5)
        stopactuator()
        break
    else:
        movement()
    
    # Reload
    if loadpattern():
        still()
        increaseactuator()
        time.delay(5)
        stopactuator()
        break
    else:
        movement()
        

def sensorcheck():
    return ((weight.sensor > weightthreshold) or timer())

def movement():
    if isEndOfTrack():
        exit()
    elif (left90() and sensorcheck()): 
        still()
        hardright()
        time.sleep(7)
        docking()
        continue
    elif (right90()): 
        hardright()
    elif leftsensor(): 
        left()
    elif rightsensor():
        right()
    else onTrack():
        straight()
        

