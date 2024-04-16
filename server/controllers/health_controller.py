from http import HTTPStatus
from typing import Callable, Awaitable, Dict

from aioredis import Redis
from fastapi import HTTPException
from genie_common.tools import logger
from genie_datastores.postgres.operations import execute_query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.responses import JSONResponse


class HealthController:
    def __init__(self, db_engine: AsyncEngine, redis: Redis):
        self._db_engine = db_engine
        self._redis = redis

    async def check_server_health(self) -> JSONResponse:
        for resource_name, check_func in self._health_checks.items():
            try:
                await check_func()

            except:
                logger.exception(f"Could not connect to {resource_name}")
                raise HTTPException(
                    status_code=HTTPStatus.SERVICE_UNAVAILABLE.value,
                    detail=f"Could not connect to `{resource_name}`"
                )

        return JSONResponse(status_code=HTTPStatus.OK.value, content={"detail": "Server is healthy"})

    @property
    def _health_checks(self) -> Dict[str, Callable[[], Awaitable[None]]]:
        return {
            "Postgres": lambda: execute_query(engine=self._db_engine, query=text("SELECT 1")),
            "Redis": lambda: self._redis.ping()
        }
