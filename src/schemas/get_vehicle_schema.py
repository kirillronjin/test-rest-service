from uuid import UUID

from pydantic import BaseModel, Field

from enums.business_type import BusinessType
from enums.type import VehicleType
from enums.vehicle_current_status import VehicleCurrentStatus


class Vehicle(BaseModel):
    id: UUID = Field(description="id")
    number_plate: str = Field(description="number_plate")
    type: VehicleType = Field(description="type")
    name: str = Field(description="type")
    business_type: BusinessType = Field(description="business_type")


class VehicleResponseData(BaseModel):
    item: Vehicle


class VehicleResponse(BaseModel):
    ok: bool
    data: VehicleResponseData
