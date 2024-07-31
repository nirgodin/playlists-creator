from typing import List, Dict

from _pytest.fixtures import fixture
from genie_common.utils import get_all_enum_values, random_alphanumeric_string
from genie_datastores.postgres.models import SpotifyTrack, TrackLyrics, AudioFeatures, BaseORMModel
from genie_datastores.models import DataSource
from genie_datastores.postgres.testing import postgres_session

from server.data.column_details import ColumnDetails
from server.data.column_group import ColumnGroup
from server.logic.columns_possible_values_querier import ColumnsPossibleValuesQuerier
from server.utils.string_utils import titleize_feature_name
from tests.server.integration.test_records import TestRecords
from tests.server.integration.test_resources import TestResources


class TestPossibleValuesQuerier:
    @fixture(autouse=True, scope="class")
    async def set_up(self, records: TestRecords):
        async with postgres_session(records.engine):
            await records.insert()
            yield

    async def test_query(self, possible_values_querier: ColumnsPossibleValuesQuerier, expected: List[ColumnDetails]):
        actual = await possible_values_querier.query()
        assert actual == expected

    @fixture(scope="class")
    def possible_values_querier(self,
                                resources: TestResources,
                                columns: List[BaseORMModel],
                                columns_descriptions: Dict[str, str]) -> ColumnsPossibleValuesQuerier:
        return ColumnsPossibleValuesQuerier(
            db_engine=resources.postgres_testkit.get_database_engine(),
            columns=columns,
            columns_descriptions=columns_descriptions
        )

    @fixture(scope="class")
    def columns(self) -> List[BaseORMModel]:
        return [
            SpotifyTrack.explicit,
            TrackLyrics.lyrics_source,
            TrackLyrics.language,
            AudioFeatures.liveness,
        ]

    @fixture(scope="class")
    def columns_descriptions(self, columns: List[BaseORMModel]) -> Dict[str, str]:
        return {column.key: random_alphanumeric_string() for column in columns}

    @fixture(scope="class")
    def expected(self,
                 tracks_lyrics: List[TrackLyrics],
                 audio_features: List[AudioFeatures],
                 columns_descriptions: Dict[str, str]) -> List[ColumnDetails]:
        liveness_values = [track.liveness for track in audio_features]
        data_sources = [titleize_feature_name(e.value) for e in get_all_enum_values(DataSource)]

        return [
            ColumnDetails(
                name=SpotifyTrack.explicit.key,
                values=["False", "True"],
                group=ColumnGroup.POSSIBLE_VALUES,
                description=columns_descriptions[SpotifyTrack.explicit.key]
            ),
            ColumnDetails(
                name=TrackLyrics.language.key,
                values=sorted({track.language for track in tracks_lyrics}),
                group=ColumnGroup.POSSIBLE_VALUES,
                description=columns_descriptions[TrackLyrics.language.key]
            ),
            ColumnDetails(
                name=AudioFeatures.liveness.key,
                values=[min(liveness_values), max(liveness_values)],
                group=ColumnGroup.MIN_MAX_VALUES,
                description=columns_descriptions[AudioFeatures.liveness.key]
            ),
            ColumnDetails(
                name=TrackLyrics.lyrics_source.key,
                values=sorted(data_sources),
                group=ColumnGroup.POSSIBLE_VALUES,
                description=columns_descriptions[TrackLyrics.lyrics_source.key]
            )
        ]
