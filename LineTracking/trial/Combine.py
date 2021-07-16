import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import Adafruit_PCA9685
import time

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

#Constants
speed = 250

def left():
    pwm.set_pwm(0, 0, 4095) # Direction L
    pwm.set_pwm(1, 0, speed) # Speed L
    pwm.set_pwm(2, 0, 0) # Direction R
    pwm.set_pwm(3, 0, speed) # Speed R

def right():
    pwm.set_pwm(0, 0, 0) # Direction L
    pwm.set_pwm(1, 0, speed) # Speed L
    pwm.set_pwm(2, 0, 4095) # Direction R
    pwm.set_pwm(3, 0, speed) # Speed R
    
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

# 7 is L, 0 is R

while True:
    if ((mcp.read_adc(2) < 600) and (mcp.read_adc(5) < 600)):
        straight()
    elif ((mcp.read_adc(0) > 600) or (mcp.read_adc(1) > 600) or (mcp.read_adc(2) > 600)): 
        right()
    elif ((mcp.read_adc(5) > 600) or (mcp.read_adc(6) > 600) or (mcp.read_adc(7) > 600)):
        left()
    else:
        still()

    # Read all the ADC channel values in a list.
    values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
    # Print the ADC values.
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
    # Pause for half a second.
    time.sleep(0.5)
    
    

