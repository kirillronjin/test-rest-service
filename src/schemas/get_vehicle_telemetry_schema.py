from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class VehicleTelemetry(BaseModel):
    id: UUID = Field(description="id")
    latitude: Optional[float] = Field(description="latitude")
    longitude: Optional[float] = Field(description="longitude")


class VehicleTelemetryResponseData(BaseModel):
    item: VehicleTelemetry


class VehicleTelemetryResponse(BaseModel):
    ok: bool
    data: VehicleTelemetryResponseData
