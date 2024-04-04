import os
from typing import Type, List, Optional

from fastapi import FastAPI, APIRouter
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware

from server.consts.env_consts import USERNAME, PASSWORD
from server.controllers.api import api_router
from server.middlewares.authentication_middleware import BasicAuthBackend
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
        return [
            Middleware(
                CORSMiddleware,
                allow_origins=[
                    "http://localhost:3000",
                ],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            ),
            Middleware(
                AuthenticationMiddleware,
                backend=BasicAuthBackend(
                    username=os.environ[USERNAME],
                    password=os.environ[PASSWORD]
                )
            )
        ]

    @staticmethod
    def _get_default_routers() -> List[APIRouter]:
        return [api_router]

    def _include_routers(self, app: FastAPI) -> None:
        for router in self._routers:
            app.include_router(router)
