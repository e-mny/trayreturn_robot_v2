from enum import Enum

class Status(Enum):
    NORMAL = 0
    UNLOAD_SEQUENCE_STARTED = 1
    WAITING_TO_UNLOAD = 2
    WAITING_TO_LOAD = 3
    WAITING_TO_MERGE = 4
    MERGING = 5