import logging
import uuid
from datetime import datetime
from math import ceil
from uuid import UUID, uuid4

from enums.type import VehicleType
from exceptions import PaginationException, \
    EntitySubordinationException, EntityAlreadyExistException
from infrastructure.repositories.db_models import category
from infrastructure.repositories.category_repo import CategoryRepository
from schemas.category_dao import CreateCategoryDAO, Category, UpdateCategoryDAO
from schemas.category_schema import CreateCategoryRequest, UpdateCategoryRequest
from settings import settings

LOGGER = logging.getLogger(__name__)


class CategoryService:
    def __init__(
            self,
            category_repo: CategoryRepository,
    ) -> None:
        self.category_repo = category_repo

    # async def get_vehicles(
    #         self,
    #         page: int,
    #         per_page: int,
    #         keyword: str,
    #         type: list[VehicleType],
    # ) -> None:
    #     """
    #     Method which returns vehicles data using VehiclesResponse schema
    #
    #     :param page: num of page
    #     :param per_page: num of records per page
    #     :param keyword: keyword for search
    #     :param type: vehicle type
    #     :param token:
    #     :return: Vehicles data
    #     """
    #
    #     if page <= 0 or per_page <= 0:
    #         LOGGER.error(msg="invalid pagination values")
    #         raise PaginationException
    #
    #     result: list[Vehicle] = []
    #
    #     vehicles_data = await self.category_repo.get_vehicles(page, per_page, keyword, type)
    #
    #     total_items_count = await self.category_repo.get_number_of_vehicles(keyword, type)
    #
    #     for vehicle_data in vehicles_data:
    #         LOGGER.info(vehicle_data)
    #         result.append(Vehicle(**vehicle_data))
    #
    #     page_count = ceil(total_items_count / per_page)
    #
    #     vehicles_response_data = VehiclesResponseData(
    #         items=vehicles_data,
    #         page=page,
    #         page_count=page_count,
    #         per_page=per_page,
    #         total_items_count=total_items_count,
    #     )
    #
    #     vehicles_response = VehiclesResponse(ok=True, data=vehicles_response_data)
    #
    #     return vehicles_response


    async def create_category(self, data: CreateCategoryRequest) -> Category:

        parent_category_id = False
        if data.parent_category_code:
            if data.parent_category_code == data.code:
                raise EntitySubordinationException(reason="a category cannot be a parent of itself")
            parent_category_id = await self.category_repo.get_category_id_without_parent_category_by_code(data.parent_category_code)

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
            parent_category_id = await self.category_repo.get_category_id_without_parent_category_by_code(data.parent_category_code)

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



