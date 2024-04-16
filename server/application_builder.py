import os
from typing import List, Optional

from fastapi import FastAPI, APIRouter
from starlette.middleware import Middleware

from server.component_factory import get_authentication_middleware, get_cors_middleware
from server.consts.env_consts import USERNAME, PASSWORD
from server.controllers.api_routes import api_router
from server.controllers.server_routes import server_router
from server.utils.general_utils import download_database


class ApplicationBuilder:
    def __init__(self,
                 middlewares: Optional[List[Middleware]] = None,
                 routers: List[APIRouter] = None):
        self._middlewares = middlewares or self._get_default_middlewares()
        self._routers = routers or self._get_default_routers()

    def build(self, should_download: bool = False) -> FastAPI:
        if should_download:
            download_database()

        app = FastAPI(middleware=self._middlewares)
        self._include_routers(app)

        return app

    @staticmethod
    def _get_default_middlewares() -> List[Middleware]:
        cors_middleware = get_cors_middleware()
        authentication_middleware = get_authentication_middleware(
            username=os.environ[USERNAME],
            password=os.environ[PASSWORD]
        )

        return [cors_middleware, authentication_middleware]

    @staticmethod
    def _get_default_routers() -> List[APIRouter]:
        return [api_router, server_router]

    def _include_routers(self, app: FastAPI) -> None:
        for router in self._routers:
            app.include_router(router)
