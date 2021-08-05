import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import Adafruit_PCA9685

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

def left_axis(speed, forward=True):
    pwm.set_pwm(1, 0, int(speed))
    if forward:
        pwm.set_pwm(0, 0, 0)
    else:
        pwm.set_pwm(0, 0, 4095)

def right_axis(speed, forward=True):
    pwm.set_pwm(3, 0, int(speed))
    if forward:
        pwm.set_pwm(2, 0, 0)
    else:
        pwm.set_pwm(2, 0, 4095)

BASE_SPEED = 500
INTEGRAL_LIMIT = 1000
kP = 1
kI = 0.2
kD = 1

try:
    previous_val = 0
    integral = 0
    while True:
        val = mcp.read_adc(3)

        error = float(500 - val)

        correction = kP * error + kI * integral + kD * (previous_val - val)
        left_val = BASE_SPEED + correction
        right_val = BASE_SPEED - correction

        if left_val > 0:
            left_axis(left_val)
        else:
            left_axis(abs(left_val), forward=False)

        if right_val > 0:
            right_axis(right_val)
        else:
            right_axis(abs(right_val), forward=False)

        integral += error
        integral = max(-INTEGRAL_LIMIT, min(INTEGRAL_LIMIT, integral))
        previous_val = val
finally:
    left_axis(0)
    right_axis(0)
    GPIO.cleanup()
