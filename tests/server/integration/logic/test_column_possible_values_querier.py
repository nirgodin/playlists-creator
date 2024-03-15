from random import randint, sample, choice
from typing import List, Dict

from _pytest.fixtures import fixture
from genie_common.utils import get_all_enum_values, random_alphanumeric_string
from genie_datastores.postgres.models import SpotifyTrack, TrackLyrics, AudioFeatures, SpotifyArtist, DataSource, \
    BaseORMModel
from genie_datastores.postgres.operations import insert_records
from genie_datastores.postgres.testing import PostgresMockFactory, postgres_session

from server.data.column_details import ColumnDetails
from server.data.column_group import ColumnGroup
from server.logic.columns_possible_values_querier import ColumnsPossibleValuesQuerier
from server.utils.string_utils import titleize_feature_name
from tests.server.integration.test_resources import TestResources


class TestPossibleValuesQuerier:
    @fixture(autouse=True, scope="class")
    async def set_up(self,
                     resources: TestResources,
                     spotify_artists: List[SpotifyArtist],
                     spotify_tracks: List[SpotifyTrack],
                     audio_features: List[AudioFeatures],
                     tracks_lyrics: List[TrackLyrics]):
        async with postgres_session(resources.engine):
            await insert_records(engine=resources.engine, records=spotify_artists)
            await insert_records(engine=resources.engine, records=spotify_tracks)
            await insert_records(engine=resources.engine, records=audio_features + tracks_lyrics)

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
    def spotify_artists(self) -> List[SpotifyArtist]:
        n_elements = randint(1, 10)
        return [PostgresMockFactory.spotify_artist() for _ in range(n_elements)]

    @fixture(scope="class")
    def spotify_tracks(self, spotify_artists: List[SpotifyArtist]) -> List[SpotifyTrack]:
        artists_ids = [artist.id for artist in spotify_artists]
        n_elements = randint(2, 10)

        return [PostgresMockFactory.spotify_track(artist_id=choice(artists_ids)) for _ in range(n_elements)]

    @fixture(scope="class")
    def tracks_lyrics(self, spotify_tracks: List[SpotifyTrack]) -> List[TrackLyrics]:
        tracks_ids = self._sample_tracks_ids(spotify_tracks)
        return [PostgresMockFactory.track_lyrics(id=id_) for id_ in tracks_ids]

    @fixture(scope="class")
    def audio_features(self, spotify_tracks: List[SpotifyTrack]) -> List[AudioFeatures]:
        tracks_ids = self._sample_tracks_ids(spotify_tracks)
        return [PostgresMockFactory.audio_features(id=id_) for id_ in tracks_ids]

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

    @staticmethod
    def _sample_tracks_ids(spotify_tracks: List[SpotifyTrack]) -> List[str]:
        n_elements = randint(2, len(spotify_tracks))
        tracks = sample(spotify_tracks, k=n_elements)

        return [track.id for track in tracks]
