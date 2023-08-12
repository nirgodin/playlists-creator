from aiohttp import ClientSession
from async_lru import alru_cache

from server.controllers.content_controllers.configuration_controller import ConfigurationController
from server.controllers.content_controllers.existing_playlist_controller import ExistingPlaylistController
from server.controllers.content_controllers.photo_controller import PhotoController
from server.controllers.content_controllers.prompt_controller import PromptController
from server.controllers.request_body_controller import RequestBodyController


@alru_cache(maxsize=1)
async def get_session() -> ClientSession:
    return await ClientSession().__aenter__()


@alru_cache(maxsize=1)
async def get_request_body_controller() -> RequestBodyController:
    return RequestBodyController()


@alru_cache(maxsize=1)
async def get_configuration_controller() -> ConfigurationController:
    session = await get_session()
    return ConfigurationController(session)


@alru_cache(maxsize=1)
async def get_prompt_controller() -> PromptController:
    session = await get_session()
    return PromptController(session)


@alru_cache(maxsize=1)
async def get_photo_controller() -> PhotoController:
    session = await get_session()
    return PhotoController(session)


@alru_cache(maxsize=1)
async def get_existing_playlist_controller() -> ExistingPlaylistController:
    session = await get_session()
    return ExistingPlaylistController(session)
