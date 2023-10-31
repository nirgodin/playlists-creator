import os
from functools import lru_cache

from aiohttp import ClientSession
from async_lru import alru_cache
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from server.consts.env_consts import USERNAME, PASSWORD
from server.controllers.content_controllers.configuration_controller import ConfigurationController
from server.controllers.content_controllers.existing_playlist_controller import ExistingPlaylistController
from server.controllers.content_controllers.photo_controller import PhotoController
from server.controllers.content_controllers.prompt_controller import PromptController
from server.controllers.request_body_controller import RequestBodyController
from server.logic.access_token_generator import AccessTokenGenerator
from server.logic.ocr.tracks_uris_image_extractor import TracksURIsImageExtractor
from server.logic.openai.embeddings_tracks_selector import EmbeddingsTracksSelector
from server.logic.openai.openai_client import OpenAIClient
from server.logic.playlist_cover_photo_creator import PlaylistCoverPhotoCreator
from server.logic.playlist_imitation.playlist_imitator import PlaylistImitator
from server.logic.playlists_creator import PlaylistsCreator
from server.logic.prompt_details_tracks_selector import PromptDetailsTracksSelector
from server.logic.spotify_tracks_collector import SpotifyTracksCollector
from server.tools.authenticator import Authenticator


@alru_cache(maxsize=1)
async def get_session() -> ClientSession:
    return await ClientSession().__aenter__()


@alru_cache(maxsize=1)
async def get_playlists_creator() -> PlaylistsCreator:
    session = await get_session()
    return PlaylistsCreator(session)


@alru_cache(maxsize=1)
async def get_playlist_cover_photo_creator() -> PlaylistCoverPhotoCreator:
    session = await get_session()
    return PlaylistCoverPhotoCreator(session)


@alru_cache(maxsize=1)
async def get_openai_client() -> OpenAIClient:
    session = await get_session()
    return OpenAIClient(session)


@alru_cache(maxsize=1)
async def get_access_token_generator() -> AccessTokenGenerator:
    session = await get_session()
    return AccessTokenGenerator(session)


@alru_cache(maxsize=1)
async def get_playlist_imitator() -> PlaylistImitator:
    session = await get_session()
    return PlaylistImitator(session)


@alru_cache(maxsize=1)
async def get_tracks_collector() -> SpotifyTracksCollector:
    session = await get_session()
    return SpotifyTracksCollector(session)


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
    playlists_cover_photo_creator = await get_playlist_cover_photo_creator()
    openai_client = await get_openai_client()
    access_token_generator = await get_access_token_generator()

    return ConfigurationController(
        playlists_creator=playlists_creator,
        playlists_cover_photo_creator=playlists_cover_photo_creator,
        openai_client=openai_client,
        access_token_generator=access_token_generator
    )


async def get_prompt_controller() -> PromptController:
    playlists_creator = await get_playlists_creator()
    playlists_cover_photo_creator = await get_playlist_cover_photo_creator()
    openai_client = await get_openai_client()
    access_token_generator = await get_access_token_generator()
    tracks_collector = await get_tracks_collector()
    prompt_details_tracks_selector = await get_prompt_details_tracks_selector()

    return PromptController(
        playlists_creator=playlists_creator,
        playlists_cover_photo_creator=playlists_cover_photo_creator,
        openai_client=openai_client,
        access_token_generator=access_token_generator,
        tracks_collector=tracks_collector,
        prompt_details_tracks_selector=prompt_details_tracks_selector
    )


async def get_photo_controller() -> PhotoController:
    playlists_creator = await get_playlists_creator()
    playlists_cover_photo_creator = await get_playlist_cover_photo_creator()
    openai_client = await get_openai_client()
    access_token_generator = await get_access_token_generator()
    tracks_uris_extractor = await get_tracks_uris_image_extractor()

    return PhotoController(
        playlists_creator=playlists_creator,
        playlists_cover_photo_creator=playlists_cover_photo_creator,
        openai_client=openai_client,
        access_token_generator=access_token_generator,
        tracks_uris_extractor=tracks_uris_extractor
    )


async def get_existing_playlist_controller() -> ExistingPlaylistController:
    playlists_creator = await get_playlists_creator()
    playlists_cover_photo_creator = await get_playlist_cover_photo_creator()
    openai_client = await get_openai_client()
    access_token_generator = await get_access_token_generator()
    playlists_imitator = await get_playlist_imitator()

    return ExistingPlaylistController(
        playlists_creator=playlists_creator,
        playlists_cover_photo_creator=playlists_cover_photo_creator,
        openai_client=openai_client,
        access_token_generator=access_token_generator,
        playlists_imitator=playlists_imitator
    )


@lru_cache(maxsize=1)
def get_authenticator() -> Authenticator:
    return Authenticator(
        username=os.environ[USERNAME],
        password=os.environ[PASSWORD]
    )
