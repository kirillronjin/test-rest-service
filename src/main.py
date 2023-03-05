import logging
from typing import Final

from atom import AtomApp
from logger import configure as configure_logger
from routers.category_router import router as vehicle_router
from settings import settings

LOGGER: Final[logging.Logger] = configure_logger("Test-rest-service")
LOGGER.info(settings)

APP_NAME = "test-rest-service"


def setup_routes(api_app: AtomApp) -> None:
    api_app.include_router(vehicle_router)


app = AtomApp(APP_NAME)
setup_routes(app)


@app.on_event("startup")
async def startup_event() -> None:
    await app.container.db().create_database()
