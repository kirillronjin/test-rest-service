from enum import Enum


class VehicleCurrentStatus(str, Enum):
    STOP: str = "stop"
    MOVEMENT: str = "movement"
    UNKNOWN: str = "unknown"
