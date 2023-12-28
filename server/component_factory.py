import os
from functools import lru_cache

from aiohttp import ClientSession
from async_lru import alru_cache
from genie_common.openai import OpenAIClient
from genie_common.tools import AioPoolExecutor
from genie_common.utils import create_client_session, build_authorization_headers
from genie_datastores.postgres.models import AudioFeatures, SpotifyArtist, SpotifyTrack, TrackLyrics, Artist
from genie_datastores.postgres.operations import get_database_engine

from server.consts.env_consts import USERNAME, PASSWORD, OPENAI_API_KEY
from server.controllers.content_controllers.configuration_controller import ConfigurationController
from server.controllers.content_controllers.existing_playlist_controller import ExistingPlaylistController
from server.controllers.content_controllers.for_you_controller import ForYouController
from server.controllers.content_controllers.photo_controller import PhotoController
from server.controllers.content_controllers.prompt_controller import PromptController
from server.controllers.content_controllers.wrapped_controller import WrappedController
from server.controllers.request_body_controller import RequestBodyController
from server.logic.configuration_photo_prompt.configuration_photo_prompt_creator import ConfigurationPhotoPromptCreator
from server.logic.configuration_photo_prompt.z_score_calculator import ZScoreCalculator
from server.logic.database_client import DatabaseClient
from server.logic.default_filter_params_generator import DefaultFilterParamsGenerator
from server.logic.ocr.artists_collector import ArtistsCollector
from server.logic.ocr.tracks_uris_image_extractor import TracksURIsImageExtractor
from server.logic.openai.columns_descriptions_creator import ColumnsDescriptionsCreator
from server.logic.openai.embeddings_tracks_selector import EmbeddingsTracksSelector
from server.logic.openai.openai_adapter import OpenAIAdapter
from server.logic.playlist_imitation.playlist_imitator import PlaylistImitator
from server.logic.playlists_creator import PlaylistsCreator
from server.logic.prompt_details_tracks_selector import PromptDetailsTracksSelector
from server.logic.columns_possible_values_querier import ColumnsPossibleValuesQuerier
from server.tools.authenticator import Authenticator


@alru_cache
async def get_session() -> ClientSession:
    session = create_client_session()
    return await session.__aenter__()


@alru_cache
async def get_playlists_creator() -> PlaylistsCreator:
    session = await get_session()
    return PlaylistsCreator(session)


@alru_cache
async def get_openai_client() -> OpenAIClient:
    api_key = os.environ[OPENAI_API_KEY]
    headers = build_authorization_headers(api_key)
    raw_session = create_client_session(headers)
    session = await raw_session.__aenter__()

    return OpenAIClient.create(session)


@alru_cache
async def get_openai_adapter() -> OpenAIAdapter:
    client = await get_openai_client()
    return OpenAIAdapter(client)


@alru_cache
async def get_playlist_imitator() -> PlaylistImitator:
    session = await get_session()
    return PlaylistImitator(session)


@alru_cache
async def get_embeddings_tracks_selector() -> EmbeddingsTracksSelector:
    openai_client = await get_openai_client()
    return EmbeddingsTracksSelector(openai_client)


@alru_cache
async def get_prompt_details_tracks_selector() -> PromptDetailsTracksSelector:
    embeddings_tracks_selector = await get_embeddings_tracks_selector()
    return PromptDetailsTracksSelector(
        embeddings_tracks_selector=embeddings_tracks_selector,
        db_client=get_database_client()
    )


@alru_cache
async def get_tracks_uris_image_extractor() -> TracksURIsImageExtractor:
    openai_adapter = await get_openai_adapter()
    pool_executor = AioPoolExecutor()

    return TracksURIsImageExtractor(
        openai_adapter=openai_adapter,
        artists_collector=ArtistsCollector(pool_executor)
    )


def get_possible_values_querier() -> ColumnsPossibleValuesQuerier:
    columns = [  # TODO: Think how to add popularity, followers, main_genre, radio_play_count, release_year
        AudioFeatures.acousticness,
        Artist.gender,
        AudioFeatures.danceability,
        AudioFeatures.duration_ms,  # TODO: Think how to transform to minutes
        AudioFeatures.energy,
        SpotifyTrack.explicit,
        AudioFeatures.instrumentalness,
        Artist.is_israeli,
        AudioFeatures.key,
        TrackLyrics.language,
        AudioFeatures.liveness,
        AudioFeatures.loudness,
        AudioFeatures.mode,
        AudioFeatures.tempo,
        AudioFeatures.time_signature,
        SpotifyTrack.number,
        AudioFeatures.valence
    ]

    return ColumnsPossibleValuesQuerier(
        db_engine=get_database_engine(),
        columns=columns
    )


@lru_cache
def get_z_score_calculator() -> ZScoreCalculator:
    return ZScoreCalculator(get_database_engine())


async def get_configuration_photo_prompt_creator() -> ConfigurationPhotoPromptCreator:
    # TODO: Think how to handle cache here
    possible_values_querier = get_possible_values_querier()
    columns_values = await possible_values_querier.query()
    default_values_generator = DefaultFilterParamsGenerator()
    params_default_values = default_values_generator.get_filter_params_defaults(columns_values)

    return ConfigurationPhotoPromptCreator(
        params_default_values=params_default_values,
        z_score_calculator=get_z_score_calculator()
    )


def get_columns_descriptions_creator():
    return ColumnsDescriptionsCreator(get_possible_values_querier())


async def get_request_body_controller() -> RequestBodyController:
    return RequestBodyController(
        possible_values_querier=get_possible_values_querier()
    )


def get_database_client() -> DatabaseClient:
    return DatabaseClient(get_database_engine())


async def get_configuration_controller() -> ConfigurationController:
    playlists_creator = await get_playlists_creator()
    openai_client = await get_openai_client()
    photo_prompt_creator = await get_configuration_photo_prompt_creator()

    return ConfigurationController(
        authenticator=get_authenticator(),
        playlists_creator=playlists_creator,
        openai_client=openai_client,
        photo_prompt_creator=photo_prompt_creator,
        db_client=get_database_client()
    )


async def get_prompt_controller() -> PromptController:
    playlists_creator = await get_playlists_creator()
    openai_client = await get_openai_client()
    openai_adapter = await get_openai_adapter()
    prompt_details_tracks_selector = await get_prompt_details_tracks_selector()

    return PromptController(
        authenticator=get_authenticator(),
        playlists_creator=playlists_creator,
        openai_client=openai_client,
        openai_adapter=openai_adapter,
        columns_descriptions_creator=get_columns_descriptions_creator(),
        prompt_details_tracks_selector=prompt_details_tracks_selector
    )


async def get_photo_controller() -> PhotoController:
    playlists_creator = await get_playlists_creator()
    openai_client = await get_openai_client()
    tracks_uris_extractor = await get_tracks_uris_image_extractor()

    return PhotoController(
        authenticator=get_authenticator(),
        playlists_creator=playlists_creator,
        openai_client=openai_client,
        tracks_uris_extractor=tracks_uris_extractor
    )


async def get_existing_playlist_controller() -> ExistingPlaylistController:
    playlists_creator = await get_playlists_creator()
    openai_client = await get_openai_client()
    playlists_imitator = await get_playlist_imitator()

    return ExistingPlaylistController(
        authenticator=get_authenticator(),
        playlists_creator=playlists_creator,
        openai_client=openai_client,
        playlists_imitator=playlists_imitator
    )


async def get_wrapped_controller() -> WrappedController:
    playlists_creator = await get_playlists_creator()
    openai_client = await get_openai_client()

    return WrappedController(
        authenticator=get_authenticator(),
        playlists_creator=playlists_creator,
        openai_client=openai_client,
    )


async def get_for_you_controller() -> ForYouController:
    playlists_creator = await get_playlists_creator()
    openai_client = await get_openai_client()
    playlists_imitator = await get_playlist_imitator()

    return ForYouController(
        authenticator=get_authenticator(),
        playlists_creator=playlists_creator,
        openai_client=openai_client,
        playlists_imitator=playlists_imitator
    )


@lru_cache
def get_authenticator() -> Authenticator:
    return Authenticator(
        username=os.environ[USERNAME],
        password=os.environ[PASSWORD]
    )
