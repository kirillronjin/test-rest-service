from typing import Optional, List

from pydantic import BaseModel, Field

from enums.sort_field import SortField


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


class GetCategoryParametersSchema(BaseModel):
    codes: Optional[List[str]] = Field(description="codes")
    name: Optional[str] = Field(description="name")
    description: Optional[str] = Field(description="description")
    parent_category_codes: Optional[List[str]] = Field(description="parentCategoryCodes")
    is_hidden: Optional[bool] = Field(description="is_hidden")
    only_parent: Optional[bool] = Field(description="only_parent")
    sort_field: Optional[SortField] = Field(description="sort_field")
    descending: Optional[bool] = Field(description="descending")
