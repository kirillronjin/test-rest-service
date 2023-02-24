from pydantic import BaseModel, Field

from schemas.get_vehicle_schema import Vehicle


class VehiclesResponseData(BaseModel):
    items: list[Vehicle] = Field(description="list of vehicles")
    page: int = Field(description="page")
    page_count: int = Field(description="page_count")
    per_page: int = Field(description="per_page")
    total_items_count: int = Field(description="total_items_count")


class VehiclesResponse(BaseModel):
    ok: bool = Field(description="ok")
    data: VehiclesResponseData
