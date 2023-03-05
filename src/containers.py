"""Containers module."""

import aiohttp
from dependency_injector import containers, providers

from database import Database
from infrastructure.repositories.category_repo import CategoryRepository
from services.category_service import CategoryService
from settings import settings


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["routers.category_router"]
    )

    config = providers.Configuration(pydantic_settings=[settings])

    db = providers.Singleton(Database, db_url=settings.get_pg_url())

    category_repo = providers.Factory(CategoryRepository, db=db.provided.engine)

    category_service = providers.Factory(
        CategoryService, category_repo
    )

