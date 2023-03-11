from pydantic import BaseModel, Field


class PageInfo(BaseModel):
    page_num: int = Field(description="page number")
    page_size: int = Field(description="number of items on the page")
    page_total: int = Field(description="total page count")
    items_count: int = Field(description="total items count")
    has_next_page: bool = Field(description="is next page available")



