from dataclasses import dataclass

from genie_common.clients.openai import OpenAIClient

from server.logic.cases_manager import CasesManager
from server.logic.playlists_creator import PlaylistsCreator
from server.tools.case_progress_reporter import CaseProgressReporter
from server.tools.spotify_session_creator import SpotifySessionCreator


@dataclass
class PlaylistCreationContext:
    playlists_creator: PlaylistsCreator
    openai_client: OpenAIClient
    session_creator: SpotifySessionCreator
    case_progress_reporter: CaseProgressReporter
    cases_manager: CasesManager
