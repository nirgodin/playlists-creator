from random import randint, choice
from typing import Union, Dict, List
from unittest.mock import AsyncMock

from _pytest.fixtures import fixture
from genie_datastores.postgres.models import PlaylistEndpoint, AudioFeatures, RadioTrack, SpotifyTrack
from spotipyio import SpotifySearchType

from server.consts.app_consts import FILTER_PARAMS
from server.controllers.content_controllers.configuration_controller import ConfigurationController
from server.data.case_status import CaseStatus
from server.data.playlist_creation_context import PlaylistCreationContext
from server.logic.configuration_photo_prompt.configuration_photo_prompt_creator import ConfigurationPhotoPromptCreator
from server.logic.database_client import DatabaseClient
from server.logic.parameters_transformer import ParametersTransformer
from server.utils.spotify_utils import to_uris
from tests.server.integration.controllers.playlist_controllers.base_playlist_controller_test import \
    BasePlaylistControllerTest


class TestConfigurationController(BasePlaylistControllerTest):
    @fixture(scope="class")
    def controller(self, context: PlaylistCreationContext, db_client: DatabaseClient) -> ConfigurationController:
        return ConfigurationController(
            context=context,
            photo_prompt_creator=AsyncMock(ConfigurationPhotoPromptCreator),
            db_client=db_client,
            parameters_transformer=ParametersTransformer()
        )

    @fixture(scope="class")
    def endpoint(self) -> PlaylistEndpoint:
        return PlaylistEndpoint.CONFIGURATION

    @fixture(scope="class")
    def payload(self, max_track_number: int) -> Dict[str, Union[str, dict]]:
        request_body = self._get_basic_request_payload()
        request_body[FILTER_PARAMS] = {
            SpotifyTrack.number.key: {
                "operator": "<=",
                "value": max_track_number
            }
        }

        return request_body

    @fixture(scope="class")
    def max_track_number(self, relevant_spotify_tracks: List[SpotifyTrack]) -> int:
        random_spotify_track = choice(relevant_spotify_tracks)
        return random_spotify_track.number

    @fixture(scope="class")
    def uris(self, relevant_spotify_tracks: List[SpotifyTrack], max_track_number: int) -> List[str]:
        track_ids = [track.id for track in relevant_spotify_tracks if track.number <= max_track_number]
        sorted_ids = sorted(track_ids)

        return to_uris(SpotifySearchType.TRACK, *sorted_ids)

    @fixture(scope="class")
    def relevant_spotify_tracks(self, radio_tracks: List[RadioTrack], spotify_tracks: List[SpotifyTrack]) -> List[SpotifyTrack]:
        radio_tracks_ids = [track.track_id for track in radio_tracks]
        return [track for track in spotify_tracks if track.id in radio_tracks_ids]

    @fixture(scope="class")
    def expected_progress_statuses(self) -> List[CaseStatus]:
        return [
            CaseStatus.CREATED,
            CaseStatus.TRACKS,
            CaseStatus.PLAYLIST,
            CaseStatus.COVER,
            CaseStatus.COMPLETED
        ]
