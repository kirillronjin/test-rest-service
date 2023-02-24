import logging
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from containers import Container
from enums.type import VehicleType
from exceptions import (
    NoDataToUpdateException,
    PaginationException,
    VehicleAlreadyExistsException,
    VehicleDoesNotExistException,
)
from schemas.create_vehicle_schema import CreateVehicleRequest
from schemas.get_vehicle_schema import VehicleResponse
from schemas.get_vehicle_telemetry_schema import VehicleTelemetryResponse
from schemas.get_vehicles_schema import VehiclesResponse
from schemas.update_vehicle_schema import UpdateVehicleRequest
from services.vehicle_service import VehiclesService
from settings import settings
from utils.generate_schemas import generate_additional_responses

LOGGER = logging.getLogger(__name__)

router = APIRouter(prefix=settings.API_URL_PREFIX, tags=["Vehicles"])


@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse,
    responses=generate_additional_responses([VehicleDoesNotExistException()]),
)
@inject
async def get_vehicle(
    vehicle_id: UUID,
    service: VehiclesService = Depends(Provide[Container.vehicle_service]),
) -> VehicleResponse:
    """
    Метод получения данных о машине

    Модель (схема) ответа - VehicleResponse
    """

    return await service.get_vehicle(vehicle_id)


@router.get("", response_model=VehiclesResponse, responses=generate_additional_responses([PaginationException()]))
@inject
async def get_vehicles(
    service: VehiclesService = Depends(Provide[Container.vehicle_service]),
    page: int = Query(default=1, description="page number"),
    per_page: int = Query(default=50, description="number of vehicles per page"),
    keyword: str = Query(default="", description="search keyword"),
    type: list[VehicleType] = Query(default=[], description="vehicle type"),
) -> VehiclesResponse:
    """
    Метод получения списка машин с поддержкой пагинации

    Модель (схема) ответа - VehiclesResponse
    """
    return await service.get_vehicles(page, per_page, keyword, type)


@router.get(
    "/{vehicle_id}/telemetry",
    response_model=VehicleTelemetryResponse,
    responses=generate_additional_responses([VehicleDoesNotExistException()]),
)
@inject
async def get_vehicle_telemetry(
    vehicle_id: UUID,
    service: VehiclesService = Depends(Provide[Container.vehicle_service]),
) -> VehicleTelemetryResponse:
    """
    Метод получения координат машины

    Модель (схема) ответа - VehicleTelemetryResponse
    """

    return await service.get_vehicle_telemetry(vehicle_id)


@router.delete(
    "/{vehicle_id}",
    responses=generate_additional_responses([VehicleDoesNotExistException()]),
)
@inject
async def delete_vehicle(
    vehicle_id: UUID,
    service: VehiclesService = Depends(Provide[Container.vehicle_service]),
) -> None:
    """
    Метод удаления машины
    """

    return await service.delete_vehicle(vehicle_id)


@router.post(
    "",
    responses=generate_additional_responses([VehicleAlreadyExistsException(), VehicleDoesNotExistException()]),
)
@inject
async def create_vehicle(
    vehicle_data: CreateVehicleRequest,
    service: VehiclesService = Depends(Provide[Container.vehicle_service]),
) -> None:
    """
    Метод создания машины

    Модель (схема) запроса (body) - CreateVehicleRequest
    """

    LOGGER.info(f"Start creating vehicle, {vehicle_data}")
    return await service.create_vehicle(vehicle_data)


@router.patch(
    "/update/{vehicle_id}",
    responses=generate_additional_responses([VehicleDoesNotExistException(), NoDataToUpdateException()]),
)
@inject
async def update_vehicle(
    vehicle_id: UUID,
    data_to_update: UpdateVehicleRequest,
    service: VehiclesService = Depends(Provide[Container.vehicle_service]),
) -> None:
    """
    Метод обновления машины

    Модель (схема) запроса (body) - UpdateVehicleRequest
    """

    return await service.update_vehicle(vehicle_id, data_to_update)
