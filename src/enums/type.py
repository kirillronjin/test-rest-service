from enum import Enum


class VehicleType(str, Enum):
    CAR: str = "car"
    MEDIUM_CARGO: str = "medium_cargo"
    CARGO: str = "cargo"
    ATOM: str = "atom"
