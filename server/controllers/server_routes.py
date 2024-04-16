from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from server.component_factory import get_health_controller
from server.controllers.health_controller import HealthController

server_router = APIRouter()


@server_router.get("/health")
async def health(health_controller: Annotated[HealthController, Depends(get_health_controller)]) -> JSONResponse:
    return await health_controller.check_server_health()
