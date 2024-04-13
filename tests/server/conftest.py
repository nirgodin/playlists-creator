from asyncio import AbstractEventLoop, new_event_loop
from typing import Generator

from _pytest.fixtures import fixture
from aiohttp import ClientSession
from aioresponses import aioresponses
from genie_common.openai import OpenAIClient
from spotipyio import SpotifyClient
from spotipyio.logic.authentication.spotify_session import SpotifySession


@fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = new_event_loop()
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
    with aioresponses() as mock_responses:
        yield mock_responses


@fixture(scope="session")
def openai_client(client_session: ClientSession) -> OpenAIClient:
    return OpenAIClient.create(client_session)
