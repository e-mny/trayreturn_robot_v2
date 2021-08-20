import Adafruit_PCA9685
from pynput.keyboard import Key, Listener

status = {
    Key.up: False,
    Key.down: False,
    Key.left: False,
    Key.right: False
}

pwm = Adafruit_PCA9685.PCA9685()

DIR_FORWARD = 0
DIR_BACKWARD = 4095

ML_DIR = 0
ML_SPEED = 1
MR_DIR = 2
MR_SPEED = 3

MAX_SPEED = 2 ** 11 - 1
OTS_SPEED = int(MAX_SPEED * 0.8)
NORMAL_SPEED = int(MAX_SPEED * 0.8)
TURN_FACTOR = int(NORMAL_SPEED * 0.5)


def move():
    dir_ = None

    if status[Key.up]:
        dir_ = DIR_FORWARD
    elif status[Key.down]:
        dir_ = DIR_BACKWARD

    if dir_ is not None:
        pwm.set_pwm(ML_DIR, 0, dir_)
        pwm.set_pwm(MR_DIR, 0, dir_)

        if status[Key.left]:
            pwm.set_pwm(ML_SPEED, 0, TURN_FACTOR)
            pwm.set_pwm(MR_SPEED, 0, NORMAL_SPEED)
        elif status[Key.right]:
            pwm.set_pwm(ML_SPEED, 0, NORMAL_SPEED)
            pwm.set_pwm(MR_SPEED, 0, TURN_FACTOR)
        else:
            pwm.set_pwm(ML_SPEED, 0, NORMAL_SPEED)
            pwm.set_pwm(MR_SPEED, 0, NORMAL_SPEED)
    else:
        # Turn on the spot (OTS)
        if status[Key.left]:
            pwm.set_pwm(ML_DIR, 0, DIR_BACKWARD)
            pwm.set_pwm(MR_DIR, 0, DIR_FORWARD)

            pwm.set_pwm(ML_SPEED, 0, OTS_SPEED)
            pwm.set_pwm(MR_SPEED, 0, OTS_SPEED)
        elif status[Key.right]:
            pwm.set_pwm(ML_DIR, 0, DIR_FORWARD)
            pwm.set_pwm(MR_DIR, 0, DIR_BACKWARD)

            pwm.set_pwm(ML_SPEED, 0, OTS_SPEED)
            pwm.set_pwm(MR_SPEED, 0, OTS_SPEED)
        else:  # Stop
            pwm.set_pwm(ML_DIR, 0, DIR_FORWARD)
            pwm.set_pwm(MR_DIR, 0, DIR_FORWARD)

            pwm.set_pwm(ML_SPEED, 0, 0)
            pwm.set_pwm(MR_SPEED, 0, 0)


def stop_moving():
    for key in status:
        status[key] = False

    move()


def on_press(key):
    if key in status and status[key] != True:
        status[key] = True
        print_status()
        move()

    # print('{0} pressed'.format(
    #     key))


def on_release(key):
    if key in status and status[key] != False:
        status[key] = False
        print_status()
        move()

    # print('{0} release'.format(
    #     key))
    if key == Key.esc:
        # Stop listener
        stop_moving()


def print_status():
    up = '^' if status[Key.up] else ' '
    down = 'v' if status[Key.down] else ' '
    left = '<' if status[Key.left] else ' '
    right = '>' if status[Key.right] else ' '

    print(
        f'\n    +---+\n'
        f'    | {up} |\n'
        f'+---+---+---+\n'
        f'| {left} | {down} | {right} |\n'
        f'+---+---+---+\n\n'
    )

# Collect events until released
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
