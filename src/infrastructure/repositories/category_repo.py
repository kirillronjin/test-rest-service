import logging
from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import func, or_, select, and_, null
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine

from exceptions import EntityNotFoundException, DatabaseException
from infrastructure.repositories.db_models import product_model, category_model, category
from schemas.category_dao import CreateCategoryDAO, Category, UpdateCategoryDAO
from schemas.category_schema import GetCategoryParametersSchema
from settings import settings

# pylint: disable=C0121

LOGGER = logging.getLogger(__name__)
#
#
from sqlalchemy.ext.asyncio import AsyncEngine


class CategoryRepository:
    def __init__(
        self,
        db: AsyncEngine,
    ) -> None:
        self._db = db

    async def get_vehicles(
        self, offset_value: int, limit_value: int, parameters: GetCategoryParametersSchema,
    ) -> list[dict[str, Any]]:
        categories_data: list[dict[str, Any]] = []

        query = (
            select(
                category
            )
            .offset((offset_value - 1) * limit_value)
            .limit(limit_value)
        )
        #
        # if parameters.name:
        #     query = query.where(category.c.name.)

        LOGGER.info(query)

        async with self._db.connect() as conn:
            query_result = await conn.execute(query)
        result = query_result.mappings().all()

        for item in result:
            categories_data.append(dict(item))

        return categories_data

    async def get_number_of_categories(self, parameters: GetCategoryParametersSchema) -> int:
        query = (
            select([func.count()])
            .select_from(category)
        )

        async with self._db.connect() as conn:
            num_of_rows = await conn.execute(query)
            return int(num_of_rows.scalar())

    async def create_category(self, category_data: CreateCategoryDAO) -> Category:
        insert_query = category.insert(dict(category_data))
        select_query = select(category).where(category.c.id == category_data.id)

        async with self._db.begin() as conn:
            try:
                await conn.execute(insert_query)

            except IntegrityError as exp:
                raise DatabaseException(reason=exp.code,
                                        details={"scenario": "CREATE"})

            result = await conn.execute(select_query)
            if created_category := result.first():
                return Category(**created_category)

    async def update_category(self, data: UpdateCategoryDAO) -> Category:
        """
        update values for vehicle in DB
        :param token:
        :param id:
        :param data_to_update: dict with data for update
        :return: bool
        """

        update_query = category.update().values(data.dict(exclude_none=True)).where((category.c.id == data.id))
        select_query = select(category).where(category.c.id == data.id)

        async with self._db.begin() as conn:
            try:
                await conn.execute(update_query)  # type: ignore

            except IntegrityError as exp:
                raise DatabaseException(reason=exp.code,
                                        details={"scenario": "UPDATE"})

            result = await conn.execute(select_query)
            if created_category := result.first():
                return Category(**created_category)

    async def get_category_id_without_parent_category_by_code(self, code: str) -> str:
        query = select(category.c.id).where(and_(category.c.code == code,
                                                 category.c.parent_category_id.is_(None)))

        async with self._db.begin() as conn:
            try:
                result = await conn.execute(query)
            except IntegrityError as exc:
                raise DatabaseException(reason=exc.code, details={"scenario": "READ"})

            if row := result.first():
                return row[0]

        raise EntityNotFoundException(reason=f"parent category with code {code} doesn't found",
                                      details={"entity_type": "category"})

    async def is_category_exist(self, category_code: str) -> bool:
        query = select(category.c.id).where(category.c.code == category_code)

        async with self._db.begin() as conn:
            result = await conn.execute(query)
            if id := result.first():
                return True

        return False

    async def get_category_id_by_code(self, code: str):
        query = select(category.c.id).where(category.c.code == code)

        async with self._db.begin() as conn:
            try:
                result = await conn.execute(query)
            except IntegrityError as exc:
                raise DatabaseException(reason=exc.code, details={"scenario": "READ"})

            if row := result.first():
                return row[0]

        raise EntityNotFoundException(reason=f"parent category with code {code} doesn't found",
                                      details={"entity_type": "category"})
