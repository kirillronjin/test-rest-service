from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from schemas.category_schema import UpdateCategoryRequest


class CreateCategoryDAO(BaseModel):
    id: UUID = Field(description="id")
    code: str = Field(description="code")
    name: str = Field(description="name")
    description: Optional[str] = Field(description="description")
    parent_category_id: Optional[UUID] = Field(description="parent_category_id")


class Category(CreateCategoryDAO):
    is_hidden: bool = Field(description="field")
    creation_date: datetime = Field(description="creation_date")
    modification_date: datetime = Field(description="creation_date")


class UpdateCategoryDAO(UpdateCategoryRequest):
    id: UUID = Field(description="id")
    parent_category_id: Optional[UUID] = Field(description="parent_category_id")
    modification_date: datetime = Field(description="datetime")
