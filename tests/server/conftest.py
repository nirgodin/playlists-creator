import asyncio

from _pytest.fixtures import fixture
from aiohttp import ClientSession
from aioresponses import aioresponses
from genie_common.clients.openai import OpenAIClient
from spotipyio import SpotifyClient
from spotipyio.logic.authentication.spotify_session import SpotifySession

from server.component_factory import get_artists_searcher
from server.logic.ocr.artists_searcher import ArtistsSearcher
from server.logic.openai.openai_adapter import OpenAIAdapter
from tests.server.consts import MILVUS_TEST_URI


@fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@fixture(scope="session")
async def client_session() -> ClientSession:
    async with ClientSession() as session:
        yield session


@fixture(scope="session")
def spotify_session(client_session: ClientSession) -> SpotifySession:
    return SpotifySession(session=client_session)


@fixture(scope="session")
def spotify_client(spotify_session: SpotifySession) -> SpotifyClient:
    return SpotifyClient.create(spotify_session)


@fixture(scope="class")
def mock_responses() -> aioresponses:
    with aioresponses(passthrough=[MILVUS_TEST_URI]) as mock_responses:
        yield mock_responses


@fixture(scope="session")
def openai_client(client_session: ClientSession) -> OpenAIClient:
    return OpenAIClient.create(client_session)


@fixture(scope="class")
def openai_adapter(openai_client: OpenAIClient) -> OpenAIAdapter:
    return OpenAIAdapter(openai_client)


@fixture(scope="class")
def artists_searcher() -> ArtistsSearcher:
    return get_artists_searcher()
