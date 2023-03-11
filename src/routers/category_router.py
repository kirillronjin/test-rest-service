import logging
from typing import List, Optional
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from containers import Container

from enums.sort_field import SortField
from exceptions import (
    EntityNotFoundException, EntitySubordinationException, PaginationException,
)
from schemas.category_dao import Category
from schemas.category_schema import CreateCategoryRequest, UpdateCategoryRequest, GetCategoryParametersSchema
from services.category_service import CategoryService
from settings import settings
from utils.generate_schemas import generate_additional_responses

LOGGER = logging.getLogger(__name__)

router = APIRouter(prefix=f"{settings.API_URL_PREFIX}/categories", tags=["Categories"])


@router.get("", responses=generate_additional_responses([PaginationException()]))
@inject
async def get_categories(
        service: CategoryService = Depends(Provide[Container.category_service]),
        page: int = Query(default=1, description="page number"),
        per_page: int = Query(default=25, description="number of categories per page"),
        codes: List[str] = Query(default=[], description="number of vehicles per page"),
        name: str = Query(default="", description="name"),
        description: str = Query(default="", description="description"),
        parent_category_codes: List[str] = Query(default=[], description="parent category codes"),
        is_hidden: bool = Query(default=None, description="is category hidden"),
        only_parent: bool = Query(default=False, description="is only parent categories"),
        sort_field: Optional[SortField] = Query(default=None, description="sort field"),
        descending: bool = Query(default=False, description="sort field")
) -> List[Category]:
    parameters = GetCategoryParametersSchema(
        codes=codes,
        name=name,
        description=description,
        parent_category_codes=parent_category_codes,
        is_hidden=is_hidden,
        only_parent=only_parent,
        sort_field=sort_field,
        descending=descending,
    )
    return await service.get_categories(page, per_page, parameters)


@router.post(
    "",
    responses=generate_additional_responses([EntitySubordinationException(), EntityNotFoundException()]),
)
@inject
async def create_category(
        data: CreateCategoryRequest,
        service: CategoryService = Depends(Provide[Container.category_service]),
) -> Category:

    return await service.create_category(data)


@router.patch(
    "/{code}",
    responses=generate_additional_responses([]),
)
@inject
async def update_category(
        code: str,
        data: UpdateCategoryRequest,
        service: CategoryService = Depends(Provide[Container.category_service]),
) -> Category:

    return await service.update_category(code, data)
