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
    # Kelvin: Middle two sensors white? Will there be a chance that this condition
    # is also satisfied when the robot is going straight? Perhaps detecting all 8
    # sensors black would be a better idea?
    return ((mcp.read_adc(3) == 0) and (mcp.read_adc(4) == 0))

def onTrack():
    # Kelvin: 2nd from middle white, and 1st from middle black?
    return ((mcp.read_adc(2) == 0) and (mcp.read_adc(5) == 0))

# Kelvin: left90 and leftsensor same pattern?
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
    # Kelvin: Why is there two load pattern? 
    if loadpattern():
        still()
        loweractuator()
        time.sleep(5)
        stopactuator()
        # Kelvin: this break doesn't do anything, remove.
        break
    # Kelvin: no need for this movement, otherwise it'll possibly
    # result in recursive calls, i.e. movement() -> docking() 
    # -> movement() -> docking() ...
    # Plus you don't actually need this, when docking() is done,
    # You will go back to the main loop, which repeatedly calls
    # the movement function.
    else:
        movement()
    
    # Reload
    if loadpattern():
        still()
        increaseactuator()
        time.delay(5)
        stopactuator()
        # Kelvin: same thing for break
        break
    # Kelvin: same thing for movement
    else:
        movement()
        

def sensorcheck():
    return ((weight.sensor > weightthreshold) or timer())

def movement():
    if isEndOfTrack():
        exit()
    elif (left90() and sensorcheck()): 
        still()

        # Kelvin: I think it's better not to use time-based instructions, i.e.
        # don't hard code the time the robot needs to turn. Do this instead
        #
        #  -----+
        #       |
        #       |
        # - If detect left90 pattern, set status to hardleft
        # - Add another condition in movement() to check for status == hardleft
        # - If status is hardleft and right sensor detects black, reset status to normal
        # - If status is hardleft and right sensor not black, hardleft()
        hardright()
        time.sleep(7)
        docking()
        # Kelvin: No need for continue, continue only works in a loop
        continue
    elif (right90()): 
        # Kelvin: where would you encounter this condition?
        hardright()
    elif leftsensor(): 
        left()
    elif rightsensor():
        right()
    # Kelvin: else statement doesn't need a condition, it is the "default condition".
    # If none of the conditions from before match, then it'll run this.
    else onTrack():
        straight()

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
        elif p == 'B' and mpc.read_adc(i) == 0:
            # If reading is white, return False because pattern does not match
            return False
        elif p == 'O' and mpc.read_adc(i) != 0:
            return False

    return True


        

