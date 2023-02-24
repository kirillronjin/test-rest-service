"""Database module."""

import logging

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from infrastructure.repositories.db_models import metadata

LOGGER = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    def __init__(self, db_url: str) -> None:
        LOGGER.info(f"Creating async engine with {db_url}")
        self.engine: AsyncEngine = create_async_engine(db_url, echo=True)

    async def create_database(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(metadata.create_all)
            LOGGER.info("Database has been updated")
