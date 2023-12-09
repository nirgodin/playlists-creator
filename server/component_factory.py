import os
from functools import lru_cache

from aiohttp import ClientSession
from async_lru import alru_cache
from genie_common.utils import create_client_session

from server.consts.env_consts import USERNAME, PASSWORD
from server.controllers.content_controllers.configuration_controller import ConfigurationController
from server.controllers.content_controllers.existing_playlist_controller import ExistingPlaylistController
from server.controllers.content_controllers.photo_controller import PhotoController
from server.controllers.content_controllers.prompt_controller import PromptController
from server.controllers.content_controllers.wrapped_controller import WrappedController
from server.controllers.request_body_controller import RequestBodyController
from server.logic.ocr.tracks_uris_image_extractor import TracksURIsImageExtractor
from server.logic.openai.embeddings_tracks_selector import EmbeddingsTracksSelector
from server.logic.openai.openai_client import OpenAIClient
from server.logic.playlist_imitation.playlist_imitator import PlaylistImitator
from server.logic.playlists_creator import PlaylistsCreator
from server.logic.prompt_details_tracks_selector import PromptDetailsTracksSelector
from server.tools.authenticator import Authenticator


@alru_cache(maxsize=1)
async def get_session() -> ClientSession:
    session = create_client_session()
    return await session.__aenter__()


@alru_cache(maxsize=1)
async def get_playlists_creator() -> PlaylistsCreator:
    session = await get_session()
    return PlaylistsCreator(session)


@alru_cache(maxsize=1)
async def get_openai_client() -> OpenAIClient:
    session = await get_session()
    return OpenAIClient(session)


@alru_cache(maxsize=1)
async def get_playlist_imitator() -> PlaylistImitator:
    session = await get_session()
    return PlaylistImitator(session)


@alru_cache(maxsize=1)
async def get_embeddings_tracks_selector() -> EmbeddingsTracksSelector:
    openai_client = await get_openai_client()
    return EmbeddingsTracksSelector(openai_client)


@alru_cache(maxsize=1)
async def get_prompt_details_tracks_selector() -> PromptDetailsTracksSelector:
    embeddings_tracks_selector = await get_embeddings_tracks_selector()
    return PromptDetailsTracksSelector(embeddings_tracks_selector)


@alru_cache(maxsize=1)
async def get_tracks_uris_image_extractor() -> TracksURIsImageExtractor:
    session = await get_session()
    return TracksURIsImageExtractor(session)


async def get_request_body_controller() -> RequestBodyController:
    return RequestBodyController()


async def get_configuration_controller() -> ConfigurationController:
    playlists_creator = await get_playlists_creator()
    openai_client = await get_openai_client()

    return ConfigurationController(
        playlists_creator=playlists_creator,
        openai_client=openai_client,
    )


async def get_prompt_controller() -> PromptController:
    playlists_creator = await get_playlists_creator()
    openai_client = await get_openai_client()
    prompt_details_tracks_selector = await get_prompt_details_tracks_selector()

    return PromptController(
        playlists_creator=playlists_creator,
        openai_client=openai_client,
        prompt_details_tracks_selector=prompt_details_tracks_selector
    )


async def get_photo_controller() -> PhotoController:
    playlists_creator = await get_playlists_creator()
    openai_client = await get_openai_client()
    tracks_uris_extractor = await get_tracks_uris_image_extractor()

    return PhotoController(
        playlists_creator=playlists_creator,
        openai_client=openai_client,
        tracks_uris_extractor=tracks_uris_extractor
    )


async def get_existing_playlist_controller() -> ExistingPlaylistController:
    playlists_creator = await get_playlists_creator()
    openai_client = await get_openai_client()
    playlists_imitator = await get_playlist_imitator()

    return ExistingPlaylistController(
        playlists_creator=playlists_creator,
        openai_client=openai_client,
        playlists_imitator=playlists_imitator
    )


async def get_wrapped_controller() -> WrappedController:
    playlists_creator = await get_playlists_creator()
    openai_client = await get_openai_client()

    return WrappedController(
        playlists_creator=playlists_creator,
        openai_client=openai_client,
    )


@lru_cache(maxsize=1)
def get_authenticator() -> Authenticator:
    return Authenticator(
        username=os.environ[USERNAME],
        password=os.environ[PASSWORD]
    )
