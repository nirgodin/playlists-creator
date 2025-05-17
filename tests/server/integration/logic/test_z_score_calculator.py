from typing import List

from _pytest.fixtures import fixture
from genie_datastores.postgres.models import SpotifyTrack, SpotifyArtist
from genie_datastores.postgres.operations import insert_records
from genie_datastores.testing.postgres import PostgresMockFactory, postgres_session

from server.logic.configuration_photo_prompt.z_score_calculator import ZScoreCalculator
from tests.server.integration.test_resources import TestResources


class TestZScoreCalculator:
    @fixture(autouse=True, scope="class")
    async def set_up(self, resources: TestResources, spotify_artist: SpotifyArtist, spotify_tracks: List[SpotifyTrack]) -> None:
        async with postgres_session(resources.engine):
            await insert_records(engine=resources.engine, records=[spotify_artist])
            await insert_records(engine=resources.engine, records=spotify_tracks)

            yield

    async def test_calculate(self, calculator: ZScoreCalculator):
        actual = await calculator.calculate(value=1, column=SpotifyTrack.number)
        assert round(actual, 2) == -2.12

    @fixture(scope="class")
    def calculator(self, resources: TestResources) -> ZScoreCalculator:
        return ZScoreCalculator(resources.engine)

    @fixture(scope="class")
    def spotify_artist(self) -> SpotifyArtist:
        return PostgresMockFactory.spotify_artist()

    @fixture(scope="class")
    def spotify_tracks(self, spotify_artist: SpotifyArtist) -> List[SpotifyTrack]:
        return [
            PostgresMockFactory.spotify_track(artist_id=spotify_artist.id, number=5),
            PostgresMockFactory.spotify_track(artist_id=spotify_artist.id, number=9)
        ]
