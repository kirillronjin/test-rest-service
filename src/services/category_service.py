import logging
import uuid
from datetime import datetime
from math import ceil
from typing import List
from uuid import UUID, uuid4

import logger
from exceptions import PaginationException, \
    EntitySubordinationException, EntityAlreadyExistException
from infrastructure.repositories.db_models import category
from infrastructure.repositories.category_repo import CategoryRepository
from schemas.category_dao import CreateCategoryDAO, Category, UpdateCategoryDAO
from schemas.category_schema import CreateCategoryRequest, UpdateCategoryRequest, GetCategoryParametersSchema
from settings import settings

LOGGER = logging.getLogger(__name__)


class CategoryService:
    def __init__(
            self,
            category_repo: CategoryRepository,
    ) -> None:
        self.category_repo = category_repo

    async def get_categories(
            self,
            page: int,
            per_page: int,
            parameters: GetCategoryParametersSchema,
    ) -> List[Category]:

        if page <= 0 or per_page <= 0:
            LOGGER.error(msg="invalid pagination values")
            raise PaginationException

        result: List[Category] = []

        categories_data = await self.category_repo.get_vehicles(page, per_page, parameters)



        total_items_count = await self.category_repo.get_number_of_categories(parameters)

        for category_data in categories_data:
            LOGGER.info(category_data)
            result.append(Category(**category_data))

        return result

    async def create_category(self, data: CreateCategoryRequest) -> Category:

        parent_category_id = False
        if data.parent_category_code:
            if data.parent_category_code == data.code:
                raise EntitySubordinationException(reason="a category cannot be a parent of itself")
            parent_category_id = await self.category_repo.get_category_id_without_parent_category_by_code(
                data.parent_category_code)

        if await self.category_repo.is_category_exist(data.code):
            raise EntityAlreadyExistException(reason=f"category eith code {data.code} is already exists",
                                              details={"entity_type": "category"})

        category_data = CreateCategoryDAO(
            id=uuid4(),
            code=data.code,
            name=data.name,
            description=data.description,
            parent_category_id=parent_category_id if parent_category_id else None,
        )

        result = await self.category_repo.create_category(category_data)
        return result

    async def update_category(self, code: str, data: UpdateCategoryRequest) -> Category:
        """
        method which update vehicle data from dict

        :param token:
        :param id: id of vehicle
        :param data_to_update: dict with data for update
        """

        category_id = await self.category_repo.get_category_id_by_code(code)

        parent_category_id = None
        if data.parent_category_code:
            if data.parent_category_code == data.code:
                raise EntitySubordinationException(reason="a category cannot be a parent of itself")
            parent_category_id = await self.category_repo.get_category_id_without_parent_category_by_code(
                data.parent_category_code)

        update_category_dao = UpdateCategoryDAO(
            id=category_id,
            code=data.code,
            name=data.name,
            description=data.description if data.description else None,
            parent_category_id=parent_category_id,
            is_hidden=data.is_hidden if data.is_hidden else None,
            modification_date=datetime.now(),
        )

        return await self.category_repo.update_category(update_category_dao)
