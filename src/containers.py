"""Containers module."""

import aiohttp
from dependency_injector import containers, providers

from database import Database
from infrastructure.repositories.vehicle_repo import VehiclesRepository
from services.vehicle_service import VehiclesService
from settings import settings


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["routers.vehicle_router"]
    )

    config = providers.Configuration(pydantic_settings=[settings])

    db = providers.Singleton(Database, db_url=settings.get_pg_url())

    vehicle_repo = providers.Factory(VehiclesRepository, db=db.provided.engine)

    vehicle_service = providers.Factory(
        VehiclesService, vehicle_repo
    )

