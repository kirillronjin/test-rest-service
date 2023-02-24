from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette_prometheus import PrometheusMiddleware

from containers import Container
from exception_handlers import handlers


class AtomApp(FastAPI):
    container: Container

    def __init__(self, app_name: str):
        super().__init__(
            title=app_name,
            default_response_class=ORJSONResponse,
            docs_url=f"/api/{app_name}/docs",
            openapi_url=f"/api/{app_name}/openapi.json",
            exception_handlers=handlers,
            swagger_ui_oauth2_redirect_url=f"/api/{app_name}/docs/oauth2-redirect",
        )
        self.container = Container()

        self.add_middleware(PrometheusMiddleware)
