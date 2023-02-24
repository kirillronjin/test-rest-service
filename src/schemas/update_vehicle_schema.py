from pydantic import BaseModel, Field

from enums.business_type import BusinessType
from enums.type import VehicleType


class UpdateVehicleRequest(BaseModel):
    name: str = Field(description="name")
    number_plate: str = Field(description="number_plate")
    type: VehicleType = Field(description="type")
    business_type: BusinessType = Field(description="type")
