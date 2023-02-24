import logging
import uuid
from datetime import datetime
from math import ceil
from uuid import UUID, uuid4

from enums.type import VehicleType
from exceptions import NoDataToUpdateException, PaginationException, VehicleDoesNotExistException
from infrastructure.repositories.db_models import vehicles
from infrastructure.repositories.vehicle_repo import VehiclesRepository
from schemas.create_vehicle_schema import CreateVehicleRequest
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


class VehiclesService:
    def __init__(
        self,
        vehicles_repo: VehiclesRepository,
    ) -> None:
        self.vehicles_repo = vehicles_repo

    async def get_vehicle(self, vehicle_id: UUID) -> VehicleResponse:
        """
        method which returns vehicle by vehicle_id and user info if needed

        :param token:
        :param vehicle_id: id of vehicle
        :return: data about vehicle
        """
        vehicle_data = await self.vehicles_repo.get_vehicle(vehicle_id)

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

        vehicles_data = await self.vehicles_repo.get_vehicles(page, per_page, keyword, type)

        total_items_count = await self.vehicles_repo.get_number_of_vehicles(keyword, type)

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

        vehicle_data = await self.vehicles_repo.get_vehicle_data_for_get_telemetry(vehicle_id)

        vehicle_telemetry_data = VehicleTelemetry(**vehicle_data)

        vehicles_response_data = VehicleTelemetryResponseData(
            item=vehicle_telemetry_data,
        )

        vehicle_response = VehicleTelemetryResponse(ok=True, data=vehicles_response_data)

        return vehicle_response

    async def create_vehicle(self, vehicle_request: CreateVehicleRequest) -> None:
        vehicle_data = vehicle_request.dict()

        vehicle_id = vehicle_data["vehicle_id"]

        if portal_vehicle_id := await self.vehicles_repo.is_vehicle_deleted(vehicle_id):
            return await self.vehicles_repo.update_vehicle_without_org_id(portal_vehicle_id, vehicle_data)

        vehicle_data.update(
            {
                vehicles.c.id: uuid4(),
                vehicles.c.org_id: uuid4(),
                vehicles.c.created_at: datetime.now(),
                vehicles.c.created_by: "1",
                vehicles.c.updated_at: datetime.now(),
                vehicles.c.updated_by: "1",
            }
        )

        await self.vehicles_repo.create_vehicle(vehicle_data)

    async def delete_vehicle(self, vehicle_id: UUID) -> None:
        """
        Method for deleting vehicle

        :param: vehicle_id: id of vehicle
        :return: BaseVehicleResponse
        """
        await self.vehicles_repo.delete_vehicle(vehicle_id)

        LOGGER.info(f"vehicle with vehicle_id={vehicle_id} was deleted")

    async def update_vehicle(self, id: UUID, data_to_update: UpdateVehicleRequest) -> None:
        """
        method which update vehicle data from dict

        :param token:
        :param id: id of vehicle
        :param data_to_update: dict with data for update
        """
        if data_to_update_dict := data_to_update.dict(exclude_none=True):
            await self.vehicles_repo.update_vehicle(id, data_to_update_dict)
            return
        raise NoDataToUpdateException
