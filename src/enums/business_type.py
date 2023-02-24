from enum import Enum


class BusinessType(str, Enum):
    TAXI: str = "taxi"
    CARSHARING: str = "carsharing"
    DELIVERY: str = "delivery"
    NO_TYPE: str = "no type"
