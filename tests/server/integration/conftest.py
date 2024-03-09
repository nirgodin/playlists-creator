from _pytest.fixtures import fixture
from genie_datastores.postgres.models import SpotifyTrack, Artist, TrackLyrics, AudioFeatures

from server.logic.columns_possible_values_querier import ColumnsPossibleValuesQuerier
from tests.server.integration.test_resources import TestResources


@fixture(scope="session")
def resources() -> TestResources:
    with TestResources() as test_resources:
        yield test_resources


@fixture(scope="session")
def possible_values_querier(resources: TestResources) -> ColumnsPossibleValuesQuerier:
    return ColumnsPossibleValuesQuerier(
        db_engine=resources.postgres_testkit.get_database_engine(),
        columns=[
            SpotifyTrack.explicit,
            TrackLyrics.lyrics_source,
            TrackLyrics.language,
            AudioFeatures.liveness,
        ]
    )
