import os
from functools import lru_cache
from http import HTTPStatus
from typing import Dict, List, Optional

from aiohttp import ClientSession
from async_lru import alru_cache
from genie_common.clients.openai import OpenAIClient
from genie_common.tools import AioPoolExecutor
from genie_common.clients.utils import create_client_session, build_authorization_headers
from genie_datastores.milvus import MilvusClient
from genie_datastores.milvus.operations import get_milvus_uri, get_milvus_token
from genie_datastores.postgres.models import PlaylistEndpoint
from genie_datastores.redis.operations import get_redis
from spotipyio import AccessTokenGenerator, EntityMatcher, SearchResultArtistEntityExtractor
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from server.consts.env_consts import OPENAI_API_KEY, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, \
    SPOTIPY_REDIRECT_URI
from server.controllers.case_controller import CasesController
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.controllers.content_controllers.configuration_controller import ConfigurationController
from server.controllers.content_controllers.existing_playlist_controller import ExistingPlaylistController
from server.controllers.content_controllers.for_you_controller import ForYouController
from server.controllers.content_controllers.photo_controller import PhotoController
from server.controllers.content_controllers.prompt_controller import PromptController
from server.controllers.content_controllers.wrapped_controller import WrappedController
from server.controllers.health_controller import HealthController
from server.controllers.request_body_controller import RequestBodyController
from server.data.playlist_creation_context import PlaylistCreationContext
from server.logic.cases_manager import CasesManager
from server.logic.columns_possible_values_querier import ColumnsPossibleValuesQuerier
from server.logic.configuration_photo_prompt.configuration_photo_prompt_creator import ConfigurationPhotoPromptCreator
from server.logic.configuration_photo_prompt.z_score_calculator import ZScoreCalculator
from server.logic.data_collection.spotify_playlist_details_collector import PlaylistDetailsCollector
from server.logic.database_client import DatabaseClient
from server.logic.default_filter_params_generator import DefaultFilterParamsGenerator
from server.logic.ocr.artists_searcher import ArtistsSearcher
from server.logic.ocr.image_text_extractor import ImageTextExtractor
from server.logic.openai.columns_descriptions_creator import ColumnsDescriptionsCreator
from server.logic.openai.openai_adapter import OpenAIAdapter
from server.logic.playlist_imitation.playlist_imitator import PlaylistImitator
from server.logic.playlist_imitation.playlist_imitator_database_filterer import PlaylistImitatorDatabaseFilterer
from server.logic.playlist_imitation.playlist_imitator_tracks_selector import PlaylistImitatorTracksSelector
from server.logic.playlists_creator import PlaylistsCreator
from server.logic.prompt.prompt_serialization_manager import PromptSerializationManager
from server.logic.prompt.prompt_serializer_interface import IPromptSerializer
from server.logic.prompt.query_conditions_prompt_serializer import QueryConditionsPromptSerializer
from server.logic.prompt.tracks_names_prompt_serializer import TracksNamesPromptSerializer
from server.logic.prompt_details_tracks_selector import PromptDetailsTracksSelector
from server.logic.similarity_scores_computer import SimilarityScoresComputer
from server.middlewares.authentication_middleware import BasicAuthBackend
from server.tools.cached_token_generator import CachedTokenGenerator
from server.tools.case_progress_reporter import CaseProgressReporter
from server.tools.spotify_session_creator import SpotifySessionCreator
from server.utils.data_utils import get_columns_descriptions, get_possible_values_columns, get_orm_conditions_map


@alru_cache
async def get_session() -> ClientSession:
    session = create_client_session()
    return await session.__aenter__()


@alru_cache
async def get_playlists_creator() -> PlaylistsCreator:
    session = await get_session()
    return PlaylistsCreator(
        session=session,
        case_progress_reporter=get_case_progress_reporter()
    )


@alru_cache
async def get_openai_client() -> OpenAIClient:
    api_key = os.environ[OPENAI_API_KEY]
    headers = build_authorization_headers(api_key)
    raw_session = create_client_session(headers)
    session = await raw_session.__aenter__()

    return OpenAIClient.create(session)


@alru_cache
async def get_openai_adapter() -> OpenAIAdapter:
    openai_client = await get_openai_client()
    return OpenAIAdapter(openai_client)


@alru_cache
async def get_playlist_imitator() -> PlaylistImitator:
    session = await get_session()
    return PlaylistImitator(
        session=session,
        case_progress_reporter=get_case_progress_reporter(),
        tracks_selector=PlaylistImitatorTracksSelector(
            database_filterer=PlaylistImitatorDatabaseFilterer(),
            similarity_scores_computer=SimilarityScoresComputer()
        )
    )


async def get_milvus_client() -> MilvusClient:
    client = MilvusClient(
        uri=get_milvus_uri(),
        token=get_milvus_token()
    )
    return await client.__aenter__()


@alru_cache
async def get_prompt_details_tracks_selector() -> PromptDetailsTracksSelector:
    milvus_client = await get_milvus_client()
    openai_client = await get_openai_client()

    return PromptDetailsTracksSelector(
        db_client=get_database_client(),
        openai_client=openai_client,
        milvus_client=milvus_client,
    )


def get_artists_searcher() -> ArtistsSearcher:
    pool_executor = AioPoolExecutor()
    entity_matcher = EntityMatcher(
        extractors={SearchResultArtistEntityExtractor(): 1},
        min_present_fields=1,
        threshold=0.8
    )

    return ArtistsSearcher(pool_executor, entity_matcher)


def get_image_text_extractor() -> ImageTextExtractor:
    return ImageTextExtractor()


def get_possible_values_querier() -> ColumnsPossibleValuesQuerier:
    return ColumnsPossibleValuesQuerier(
        db_engine=get_database_engine(),
        columns=get_possible_values_columns(),
        columns_descriptions=get_columns_descriptions()
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
    return DatabaseClient(
        db_engine=get_database_engine(),
        columns=get_possible_values_columns(),
        orm_conditions_map=get_orm_conditions_map()
    )


@alru_cache
async def get_access_token_generator() -> AccessTokenGenerator:
    session = await get_session()
    return AccessTokenGenerator(
        client_id=os.environ[SPOTIPY_CLIENT_ID],
        client_secret=os.environ[SPOTIPY_CLIENT_SECRET],
        redirect_uri=os.environ[SPOTIPY_REDIRECT_URI],
        session=session
    )


@alru_cache
async def get_spotify_session_creator() -> SpotifySessionCreator:
    access_token_generator = await get_access_token_generator()
    cached_token_generator = CachedTokenGenerator(access_token_generator)

    return SpotifySessionCreator(cached_token_generator)


async def get_configuration_controller() -> ConfigurationController:
    context = await get_playlist_creation_context()
    photo_prompt_creator = await get_configuration_photo_prompt_creator()

    return ConfigurationController(
        context=context,
        photo_prompt_creator=photo_prompt_creator,
        db_client=get_database_client(),
    )


async def get_prompt_controller() -> PromptController:
    context = await get_playlist_creation_context()
    prompt_details_tracks_selector = await get_prompt_details_tracks_selector()
    serialization_manager = await get_prompt_serialization_manager()

    return PromptController(
        context=context,
        prompt_details_tracks_selector=prompt_details_tracks_selector,
        serialization_manager=serialization_manager
    )


async def get_prompt_serialization_manager() -> PromptSerializationManager:
    openai_adapter = await get_openai_adapter()
    prioritized_serializers = await get_prioritized_prompt_serializers()

    return PromptSerializationManager(
        prioritized_serializers=prioritized_serializers,
        openai_adapter=openai_adapter
    )


async def get_query_conditions_prompt_serializer(descriptions_creator: Optional[ColumnsDescriptionsCreator]) -> QueryConditionsPromptSerializer:
    if descriptions_creator is None:
        descriptions_creator = get_columns_descriptions_creator()

    columns_details = await descriptions_creator.create()
    return QueryConditionsPromptSerializer(columns_details)


async def get_prioritized_prompt_serializers(descriptions_creator: Optional[ColumnsDescriptionsCreator] = None) -> List[IPromptSerializer]:
    query_conditions_prompt_serializer = await get_query_conditions_prompt_serializer(descriptions_creator)
    return [
        query_conditions_prompt_serializer,
        TracksNamesPromptSerializer()
    ]


async def get_photo_controller() -> PhotoController:
    context = await get_playlist_creation_context()
    openai_adapter = await get_openai_adapter()

    return PhotoController(
        context=context,
        image_text_extractor=get_image_text_extractor(),
        openai_adapter=openai_adapter,
        artists_searcher=get_artists_searcher()
    )


@alru_cache
async def get_playlist_creation_context() -> PlaylistCreationContext:
    playlists_creator = await get_playlists_creator()
    openai_client = await get_openai_client()
    spotify_session = await get_spotify_session_creator()
    case_progress_reporter = get_case_progress_reporter()
    cases_manager = get_cases_manager()

    return PlaylistCreationContext(
        playlists_creator=playlists_creator,
        openai_client=openai_client,
        session_creator=spotify_session,
        case_progress_reporter=case_progress_reporter,
        cases_manager=cases_manager
    )


async def get_existing_playlist_controller() -> ExistingPlaylistController:
    context = await get_playlist_creation_context()
    playlists_imitator = await get_playlist_imitator()

    return ExistingPlaylistController(
        context=context,
        playlists_imitator=playlists_imitator,
        playlist_details_collector=get_playlist_details_collector()
    )


async def get_wrapped_controller() -> WrappedController:
    context = await get_playlist_creation_context()
    return WrappedController(context)


async def get_for_you_controller() -> ForYouController:
    context = await get_playlist_creation_context()
    playlists_imitator = await get_playlist_imitator()

    return ForYouController(
        context=context,
        playlists_imitator=playlists_imitator,
        playlist_details_collector=get_playlist_details_collector()
    )


def get_playlist_details_collector() -> PlaylistDetailsCollector:
    return PlaylistDetailsCollector(get_case_progress_reporter())


def get_cases_controller() -> CasesController:
    return CasesController(get_cases_manager())


def get_cases_manager() -> CasesManager:
    return CasesManager(
        db_engine=get_database_engine(),
        case_progress_reporter=get_case_progress_reporter()
    )


async def get_endpoint_controller_mapping() -> Dict[PlaylistEndpoint, BaseContentController]:
    return {
        PlaylistEndpoint.CONFIGURATION: await get_configuration_controller(),
        PlaylistEndpoint.EXISTING_PLAYLIST: await get_existing_playlist_controller(),
        PlaylistEndpoint.FOR_YOU: await get_for_you_controller(),
        PlaylistEndpoint.PHOTO: await get_photo_controller(),
        PlaylistEndpoint.PROMPT: await get_prompt_controller(),
        PlaylistEndpoint.WRAPPED: await get_wrapped_controller(),
    }


def get_case_progress_reporter() -> CaseProgressReporter:
    return CaseProgressReporter(get_database_engine())


def get_authentication_middleware(username: str, password: str) -> Middleware:
    backend = BasicAuthBackend(
        username=username,
        password=password
    )
    return Middleware(
        AuthenticationMiddleware,
        backend=backend,
        on_error=lambda conn, exc: JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED.value,
            content={"message": "Unauthorized"}
        )
    )


def get_cors_middleware() -> Middleware:
    return Middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


async def get_health_controller() -> HealthController:
    milvus = await get_milvus_client()
    return HealthController(
        db_engine=get_database_engine(),
        redis=get_redis(),
        milvus=milvus
    )


@lru_cache
def get_database_engine() -> AsyncEngine:
    return create_async_engine(os.environ["GENIE_DATABASE_URL"])
