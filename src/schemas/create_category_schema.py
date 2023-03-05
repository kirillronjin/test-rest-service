from typing import Optional

from pydantic import BaseModel, Field


class CreateCategoryRequest(BaseModel):
    code: str = Field(description="name", min_length=1)
    name: str = Field(description="name", min_length=1)
    description: Optional[str] = Field(description="name")
    parent_category_code: Optional[str] = Field(description="name")
