from typing import List, Set

from _pytest.fixtures import fixture
from genie_common.utils import random_boolean
from genie_datastores.postgres.models import RadioTrack, AudioFeatures, SpotifyTrack, Artist
from genie_datastores.postgres.testing import postgres_session

from server.data.query_condition import QueryCondition
from server.logic.database_client import DatabaseClient
from tests.server.integration.test_records import TestRecords


class TestDatabaseClient:
    @fixture(autouse=True, scope="class")
    async def set_up(self, records: TestRecords) -> None:
        async with postgres_session(records.engine):
            await records.insert()
            yield

    async def test_query__no_conditions__returns_all(self,
                                                     db_client: DatabaseClient,
                                                     radio_tracks: List[RadioTrack]):
        expected = {track.track_id for track in radio_tracks}
        actual = await db_client.query([])
        assert sorted(expected) == sorted(actual)

    async def test_query__no_condition_met__returns_empty_list(self,
                                                               db_client: DatabaseClient,
                                                               audio_features: List[AudioFeatures]):
        tracks_valence = [track.valence for track in audio_features]
        condition = QueryCondition(
            column=AudioFeatures.valence.key,
            operator=">=",
            value=max(tracks_valence) + 1
        )

        actual = await db_client.query([condition])

        assert actual == []

    async def test_query__single_condition_met__returns_expected_ids(self,
                                                                     db_client: DatabaseClient,
                                                                     artists: List[Artist],
                                                                     radio_tracks: List[RadioTrack],
                                                                     spotify_tracks: List[SpotifyTrack]):
        expected_is_israeli = random_boolean()
        expected = self._get_expected_single_condition_tracks_ids(
            expected_is_israeli=expected_is_israeli,
            artists=artists,
            radio_tracks=radio_tracks,
            spotify_tracks=spotify_tracks
        )
        condition = QueryCondition(
            column=Artist.is_israeli.key,
            operator="in",
            value=[expected_is_israeli]
        )

        actual = await db_client.query([condition])

        assert sorted(actual) == sorted(expected)

    @staticmethod
    def _get_expected_single_condition_tracks_ids(expected_is_israeli: bool,
                                                  artists: List[Artist],
                                                  radio_tracks: List[RadioTrack],
                                                  spotify_tracks: List[SpotifyTrack]) -> Set[str]:
        artists_ids = [artist.id for artist in artists if artist.is_israeli == expected_is_israeli]
        tracks_ids = [track.id for track in spotify_tracks if track.artist_id in artists_ids]

        return {track.track_id for track in radio_tracks if track.track_id in tracks_ids}
