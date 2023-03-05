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
from schemas.category_dao import CreateCategoryDAO, Category
from schemas.create_category_schema import CreateCategoryRequest
from schemas.get_vehicle_schema import Vehicle, VehicleResponse, VehicleResponseData
from schemas.get_vehicle_telemetry_schema import (
    VehicleTelemetry,
    VehicleTelemetryResponse,
    VehicleTelemetryResponseData,
)
from schemas.get_vehicles_schema import VehiclesResponse, VehiclesResponseData
from schemas.update_vehicle_schema import UpdateVehicleRequest
from settings import settings

LOGGER = logging.getLogger(__name__)


class CategoryService:
    def __init__(
            self,
            category_repo: CategoryRepository,
    ) -> None:
        self.category_repo = category_repo

    async def get_vehicle(self, vehicle_id: UUID) -> VehicleResponse:
        """
        method which returns vehicle by vehicle_id and user info if needed

        :param token:
        :param vehicle_id: id of vehicle
        :return: data about vehicle
        """
        vehicle_data = await self.category_repo.get_vehicle(vehicle_id)

        LOGGER.info(vehicle_data)
        vehicle = Vehicle(**vehicle_data)

        vehicle_response_data = VehicleResponseData(item=vehicle)
        vehicle_response = VehicleResponse(ok=True, data=vehicle_response_data)

        return vehicle_response

    async def get_vehicles(
            self,
            page: int,
            per_page: int,
            keyword: str,
            type: list[VehicleType],
    ) -> VehiclesResponse:
        """
        Method which returns vehicles data using VehiclesResponse schema

        :param page: num of page
        :param per_page: num of records per page
        :param keyword: keyword for search
        :param type: vehicle type
        :param token:
        :return: Vehicles data
        """

        if page <= 0 or per_page <= 0:
            LOGGER.error(msg="invalid pagination values")
            raise PaginationException

        result: list[Vehicle] = []

        vehicles_data = await self.category_repo.get_vehicles(page, per_page, keyword, type)

        total_items_count = await self.category_repo.get_number_of_vehicles(keyword, type)

        for vehicle_data in vehicles_data:
            LOGGER.info(vehicle_data)
            result.append(Vehicle(**vehicle_data))

        page_count = ceil(total_items_count / per_page)

        vehicles_response_data = VehiclesResponseData(
            items=vehicles_data,
            page=page,
            page_count=page_count,
            per_page=per_page,
            total_items_count=total_items_count,
        )

        vehicles_response = VehiclesResponse(ok=True, data=vehicles_response_data)

        return vehicles_response

    async def get_vehicle_telemetry(self, vehicle_id: UUID) -> VehicleTelemetryResponse:
        """
        Method which returns vehicles data using VehiclesResponse schema

        :param vehicle_id:
        :param token:
        :return: Vehicles data
        """

        vehicle_data = await self.category_repo.get_vehicle_data_for_get_telemetry(vehicle_id)

        vehicle_telemetry_data = VehicleTelemetry(**vehicle_data)

        vehicles_response_data = VehicleTelemetryResponseData(
            item=vehicle_telemetry_data,
        )

        vehicle_response = VehicleTelemetryResponse(ok=True, data=vehicles_response_data)

        return vehicle_response

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

    async def delete_vehicle(self, vehicle_id: UUID) -> None:
        """
        Method for deleting vehicle

        :param: vehicle_id: id of vehicle
        :return: BaseVehicleResponse
        """
        await self.category_repo.delete_vehicle(vehicle_id)

        LOGGER.info(f"vehicle with vehicle_id={vehicle_id} was deleted")

    async def update_vehicle(self, id: UUID, data_to_update: UpdateVehicleRequest) -> None:
        """
        method which update vehicle data from dict

        :param token:
        :param id: id of vehicle
        :param data_to_update: dict with data for update
        """
        if data_to_update_dict := data_to_update.dict(exclude_none=True):
            await self.category_repo.update_vehicle(id, data_to_update_dict)
            return

