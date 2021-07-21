import Direction
from Direction import movement, debug
from Status import Status

if __name__ == "__main__":
    x = 0
    status = Status.NORMAL

    while True:
        debug()
        status = movement(status)
