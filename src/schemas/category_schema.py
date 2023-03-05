from typing import Optional

from pydantic import BaseModel, Field


class CreateCategoryRequest(BaseModel):
    code: str = Field(description="code", min_length=1)
    name: str = Field(description="name", min_length=1)
    description: Optional[str] = Field(description="description")
    parent_category_code: Optional[str] = Field(description="parent_category_code")


class UpdateCategoryRequest(BaseModel):
    code: str = Field(description="code", min_length=1)
    name: Optional[str] = Field(description="name", min_length=1)
    description: Optional[str] = Field(description="description")
    parent_category_code: Optional[str] = Field(description="parent_category_code")
    is_hidden: Optional[bool] = Field(description="is_hidden")
