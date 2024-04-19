from http import HTTPStatus
from inspect import iscoroutinefunction
from typing import Callable, Awaitable, Dict, Optional

from redis import Redis
from fastapi import HTTPException
from genie_common.tools import logger
from genie_datastores.milvus import MilvusClient
from genie_datastores.postgres.operations import execute_query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.responses import JSONResponse


class HealthController:
    def __init__(self, db_engine: AsyncEngine, redis: Redis, milvus: MilvusClient):
        self._db_engine = db_engine
        self._redis = redis
        self._milvus = milvus

    async def check_server_health(self) -> JSONResponse:
        for resource_name, check_func in self._health_checks.items():
            try:
                await self._execute_health_check(check_func)

            except:
                logger.exception(f"Could not connect to {resource_name}")
                raise HTTPException(
                    status_code=HTTPStatus.SERVICE_UNAVAILABLE.value,
                    detail=f"Could not connect to `{resource_name}`"
                )

        return JSONResponse(status_code=HTTPStatus.OK.value, content={"detail": "Server is healthy"})

    @staticmethod
    async def _execute_health_check(check_func: Callable[[], Optional[Awaitable[None]]]) -> None:
        if iscoroutinefunction(check_func):
            await check_func()
        else:
            check_func()

    @property
    def _health_checks(self) -> Dict[str, Callable[[], Optional[Awaitable[None]]]]:
        return {
            "Postgres": self._is_postgres_healthy,
            "Redis": self._redis.ping,
            "Milvus": self._milvus.collections.list
        }

    async def _is_postgres_healthy(self) -> None:
        await execute_query(engine=self._db_engine, query=text("SELECT 1"))
