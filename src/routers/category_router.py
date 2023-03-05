import logging
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from containers import Container
from enums.type import VehicleType
from exceptions import (
    EntityNotFoundException, EntitySubordinationException,
)
from schemas.category_dao import Category
from schemas.category_schema import CreateCategoryRequest, UpdateCategoryRequest
from services.category_service import CategoryService
from settings import settings
from utils.generate_schemas import generate_additional_responses

LOGGER = logging.getLogger(__name__)

router = APIRouter(prefix=f"{settings.API_URL_PREFIX}/categories", tags=["Categories"])


# @router.get(
#     "/{vehicle_id}",
#     response_model=VehicleResponse,
#     responses=generate_additional_responses([VehicleDoesNotExistException()]),
# )
# @inject
# async def get_vehicle(
#     vehicle_id: UUID,
#     service: CategoryService = Depends(Provide[Container.category_service]),
# ) -> VehicleResponse:
#     """
#     Метод получения данных о машине
#
#     Модель (схема) ответа - VehicleResponse
#     """
#
#     return await service.get_vehicle(vehicle_id)

#
# @router.get("", response_model=VehiclesResponse, responses=generate_additional_responses([PaginationException()]))
# @inject
# async def get_vehicles(
#     service: CategoryService = Depends(Provide[Container.category_service]),
#     page: int = Query(default=1, description="page number"),
#     per_page: int = Query(default=50, description="number of vehicles per page"),
#     keyword: str = Query(default="", description="search keyword"),
#     type: list[VehicleType] = Query(default=[], description="vehicle type"),
# ) -> VehiclesResponse:
#     """
#     Метод получения списка машин с поддержкой пагинации
#
#     Модель (схема) ответа - VehiclesResponse
#     """
#     return await service.get_vehicles(page, per_page, keyword, type)
#
#
# @router.delete(
#     "/{vehicle_id}",
#     responses=generate_additional_responses([VehicleDoesNotExistException()]),
# )
# @inject
# async def delete_vehicle(
#     vehicle_id: UUID,
#     service: CategoryService = Depends(Provide[Container.category_service]),
# ) -> None:
#     """
#     Метод удаления машины
#     """
#
#     return await service.delete_vehicle(vehicle_id)


@router.post(
    "",
    responses=generate_additional_responses([EntitySubordinationException(), EntityNotFoundException()]),
)
@inject
async def create_category(
        data: CreateCategoryRequest,
        service: CategoryService = Depends(Provide[Container.category_service]),
) -> Category:
    """
    Метод создания машины

    Модель (схема) запроса (body) - CreateVehicleRequest
    """

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
    """
    Метод обновления машины

    Модель (схема) запроса (body) - UpdateVehicleRequest
    """

    return await service.update_category(code, data)
