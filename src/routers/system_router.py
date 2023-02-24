from fastapi import APIRouter
from starlette_prometheus import metrics

system_router = APIRouter()
system_router.add_route("/metrics", metrics)


@system_router.get("/healthz")
async def health():
    return {"ok": True}


@system_router.get("/readyz")
async def ready():
    return {"ok": True}
