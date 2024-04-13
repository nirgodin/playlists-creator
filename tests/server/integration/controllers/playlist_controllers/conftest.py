from unittest.mock import AsyncMock

from _pytest.fixtures import fixture
from aiohttp import ClientSession
from genie_common.openai import OpenAIClient
from spotipyio.logic.authentication.spotify_session import SpotifySession

from server.data.playlist_creation_context import PlaylistCreationContext
from server.logic.cases_manager import CasesManager
from server.logic.playlists_creator import PlaylistsCreator
from server.tools.case_progress_reporter import CaseProgressReporter
from server.tools.spotify_session_creator import SpotifySessionCreator


@fixture(scope="session")
def context(cases_manager: CasesManager,
            case_progress_reporter: CaseProgressReporter,
            session_creator: AsyncMock,
            openai_client: OpenAIClient,
            playlists_creator: PlaylistsCreator) -> PlaylistCreationContext:
    return PlaylistCreationContext(
        playlists_creator=playlists_creator,
        openai_client=openai_client,
        session_creator=session_creator,
        case_progress_reporter=case_progress_reporter,
        cases_manager=cases_manager
    )


@fixture(scope="session")
def playlists_creator(client_session: ClientSession, case_progress_reporter: CaseProgressReporter) -> PlaylistsCreator:
    return PlaylistsCreator(
        session=client_session,
        case_progress_reporter=case_progress_reporter
    )


@fixture(scope="session")
def session_creator(spotify_session: SpotifySession) -> AsyncMock:
    mock_session_creator = AsyncMock(SpotifySessionCreator)
    mock_session_creator.create.return_value.__aenter__.return_value = spotify_session

    return mock_session_creator
