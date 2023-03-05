import logging
from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import func, or_, select, and_, null
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine

from enums.type import VehicleType
from exceptions import EntityNotFoundException, DatabaseException
from infrastructure.repositories.db_models import product_model, category_model, category
from schemas.category_dao import CreateCategoryDAO, Category
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

    async def is_vehicle_deleted(self, vehicle_id) -> UUID | None:
        pass
        # query = select(vehicles.c.id, vehicles.c.org_id).where(vehicles.c.vehicle_id == vehicle_id)
        #
        # async with self._db.begin() as conn:
        #     result = await conn.execute(query)
        #
        # if vehicle := result.first():
        #     vehicle_data = dict(vehicle)
        #     if not vehicle_data["org_id"]:
        #         return vehicle_data["id"]
        # return None

    async def get_vehicle(self, vehicle_id: UUID) -> dict[str, Any]:
        pass
        # query = select(
        #     vehicles.c.id,
        #     vehicles.c.icc_id,
        #     vehicles.c.number_plate,
        #     vehicles.c.type,
        #     vehicles.c.name,
        #     vehicles.c.business_type,
        # ).where((vehicles.c.id == vehicle_id) & (vehicles.c.org_id.is_not(None)))
        #
        # async with self._db.connect() as conn:
        #     result = await conn.execute(query)
        #
        # if vehicle := result.first():
        #     vehicle_data = dict(vehicle)
        #     return vehicle_data
        #
        # LOGGER.info(f"vehicle with vehicle_id={vehicle_id} not exist")
        # raise VehicleDoesNotExistException

    async def get_vehicle_data_for_get_telemetry(self, vehicle_id: UUID) -> dict[str, Any]:
        pass
        # query = select(
        #     vehicles.c.id,
        #     vehicles.c.icc_id,
        # ).where((vehicles.c.id == vehicle_id) & (vehicles.c.org_id.is_not(None)))
        #
        # async with self._db.connect() as conn:
        #     result = await conn.execute(query)
        #
        # if vehicle := result.first():
        #     vehicle_data = dict(vehicle)
        #     return vehicle_data
        #
        # LOGGER.info(f"vehicle with vehicle_id={vehicle_id} not exist")
        # raise VehicleDoesNotExistException

    async def delete_vehicle(self, vehicle_id: UUID):
        pass
        # """
        # Method which delete vehicle
        #
        # :param: vehicle_id: id of vehicle
        # """
        # delete_query = (
        #     vehicles.update()
        #     .values({vehicles.c.org_id: None})
        #     .where((vehicles.c.id == vehicle_id) & (vehicles.c.org_id.is_not(None)))
        # )
        #
        # async with self._db.begin() as conn:
        #     query_result: CursorResult = await conn.execute(delete_query)  # type: ignore
        #     if query_result.rowcount < 1:  # type: ignore
        #         LOGGER.info(f"vehicle with vehicle_id={vehicle_id} not exist")
        #         raise VehicleDoesNotExistException

    async def get_vehicles(
        self, offset_value: int, limit_value: int, keyword: str, type: list[VehicleType]
    ) -> list[dict[str, Any]]:
        pass
        # """
        # method which returns list of existing vehicles
        # :param limit_value:
        # :param offset_value:
        # :param keyword:
        # :return: list of vehicles
        # """
        # vehicles_data: list[dict[str, Any]] = []
        #
        # query = (
        #     select(
        #         vehicles.c.id,
        #         vehicles.c.icc_id,
        #         vehicles.c.number_plate,
        #         vehicles.c.type,
        #         vehicles.c.name,
        #         vehicles.c.business_type,
        #     )
        #     .where(vehicles.c.org_id.is_not(None))
        #     .filter(or_(vehicles.c.number_plate.like(f"%{keyword}%"), vehicles.c.name.like(f"%{keyword}%")))
        #     .offset((offset_value - 1) * limit_value)
        #     .limit(limit_value)
        # )
        #
        # if type:
        #     query = query.where(vehicles.c.type.in_(type))
        #
        # LOGGER.debug(query)
        #
        # async with self._db.connect() as conn:
        #     query_result = await conn.execute(query)
        # result = query_result.mappings().all()
        #
        # for vehicle in result:
        #     vehicles_data.append(dict(vehicle))
        #
        # return vehicles_data

    async def get_number_of_vehicles(self, keyword: str, type: list[VehicleType]) -> int:
        pass
        # """
        # Method which returns number of vehicles in DB
        # :return: number of vehicles
        # """
        # query = (
        #     select([func.count()])
        #     .select_from(vehicles)
        #     .where(vehicles.c.org_id.is_not(None))
        #     .filter(or_(vehicles.c.number_plate.like(f"%{keyword}%"), vehicles.c.name.like(f"%{keyword}%")))
        # )
        #
        # if type:
        #     query = query.where(vehicles.c.type.in_(type))
        #
        # async with self._db.connect() as conn:
        #     num_of_rows = await conn.execute(query)
        #     return int(num_of_rows.scalar())

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

    async def update_vehicle(self, id: UUID, data_to_update: dict[str, Any]) -> None:
        pass
        # """
        # update values for vehicle in DB
        # :param token:
        # :param id:
        # :param data_to_update: dict with data for update
        # :return: bool
        # """
        #
        #
        # data_to_update.update(
        #     {
        #         vehicles.c.updated_at: datetime.now(),
        #         vehicles.c.updated_by: "!",
        #     }
        # )
        #
        # query = vehicles.update().values(data_to_update).where((vehicles.c.id == id) & (vehicles.c.org_id.is_not(None)))
        #
        # async with self._db.begin() as conn:
        #     result: CursorResult = await conn.execute(query)  # type: ignore
        #
        #     if result.rowcount == 0:  # type: ignore
        #         raise VehicleDoesNotExistException

    async def get_category_id_without_parent_category_by_code(self, parent_category_code: str) -> str:
        query = select(category.c.id).where(and_(category.c.code == parent_category_code,
                                                 category.c.parent_category_id.is_(None)))

        async with self._db.begin() as conn:
            try:
                result = await conn.execute(query)
            except IntegrityError as exc:
                raise DatabaseException(reason=exc.code, details={"scenario": "READ"})

            if row := result.first():
                return row[0]

        raise EntityNotFoundException(reason=f"parent category with code {parent_category_code} doesn't found",
                                      details={"entity_type": "category"})

    async def is_category_exist(self, category_code: str) -> bool:
        query = select(category.c.id).where(category.c.code == category_code)

        async with self._db.begin() as conn:
            result = await conn.execute(query)
            if id := result.first():
                return True

        return False