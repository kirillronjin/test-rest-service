from uuid import UUID

from pydantic import BaseModel, Field

from enums.business_type import BusinessType
from enums.type import VehicleType


class CreateVehicleRequest(BaseModel):
    name: str = Field(description="name")
    number_plate: str = Field(description="number_plate")
    type: VehicleType = Field(description="type")
    vehicle_id: UUID = Field(description="vehicle_id")
    business_type: BusinessType = Field(description="type", default=BusinessType.NO_TYPE)
