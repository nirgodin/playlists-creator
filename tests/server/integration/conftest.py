from random import randint, choice, sample
from typing import List, Union

from _pytest.fixtures import fixture
from genie_datastores.postgres.models import SpotifyTrack, TrackLyrics, AudioFeatures, SpotifyArtist, Artist, \
    ShazamArtist, RadioTrack
from genie_datastores.postgres.testing import PostgresMockFactory

from server.logic.database_client import DatabaseClient
from server.utils.data_utils import get_possible_values_columns, get_orm_conditions_map
from tests.server.integration.test_records import TestRecords
from tests.server.integration.test_resources import TestResources


@fixture(scope="session")
async def resources() -> TestResources:
    async with TestResources() as test_resources:
        yield test_resources


@fixture(scope="session")
def db_client(resources: TestResources) -> DatabaseClient:
    return DatabaseClient(
        db_engine=resources.engine,
        columns=get_possible_values_columns(),
        orm_conditions_map=get_orm_conditions_map()
    )


@fixture(scope="class")
def records(resources: TestResources,
            spotify_artists: List[SpotifyArtist],
            artists: List[Artist],
            spotify_tracks: List[SpotifyTrack],
            radio_tracks: List[RadioTrack],
            audio_features: List[AudioFeatures],
            tracks_lyrics: List[TrackLyrics],
            shazam_artists: List[ShazamArtist]) -> TestRecords:
    return TestRecords(
        engine=resources.engine,
        spotify_artists=spotify_artists,
        shazam_artists=shazam_artists,
        artists=artists,
        spotify_tracks=spotify_tracks,
        radio_tracks=radio_tracks,
        audio_features=audio_features,
        tracks_lyrics=tracks_lyrics
    )


@fixture(scope="class")
def spotify_artists() -> List[SpotifyArtist]:
    n_elements = randint(1, 10)
    return [PostgresMockFactory.spotify_artist() for _ in range(n_elements)]


@fixture(scope="class")
def shazam_artists() -> List[ShazamArtist]:
    n_elements = randint(1, 10)
    return [PostgresMockFactory.shazam_artist() for _ in range(n_elements)]


@fixture(scope="class")
def artists(spotify_artists: List[SpotifyArtist], shazam_artists: List[ShazamArtist]) -> List[Artist]:
    n_artists = len(spotify_artists)
    shazam_artists_ids = [artist.id for artist in shazam_artists]
    spotify_ids = [artist.id for artist in spotify_artists]
    shazam_ids = [choice(shazam_artists_ids) for _ in range(n_artists)]

    return [PostgresMockFactory.artist(id=id_, shazam_id=shazam_id) for id_, shazam_id in zip(spotify_ids, shazam_ids)]


@fixture(scope="class")
def spotify_tracks(spotify_artists: List[SpotifyArtist]) -> List[SpotifyTrack]:
    artists_ids = [artist.id for artist in spotify_artists]
    n_elements = randint(2, 10)

    return [PostgresMockFactory.spotify_track(artist_id=choice(artists_ids)) for _ in range(n_elements)]


@fixture(scope="class")
def radio_tracks(spotify_tracks: List[SpotifyTrack]) -> List[RadioTrack]:
    tracks_ids = [track.id for track in spotify_tracks]
    n_elements = len(spotify_tracks) * randint(1, 5)

    return [PostgresMockFactory.radio_track(track_id=choice(tracks_ids)) for _ in range(n_elements)]


@fixture(scope="class")
def tracks_lyrics(spotify_tracks: List[SpotifyTrack]) -> List[TrackLyrics]:
    tracks_ids = _sample_spotify_ids(spotify_tracks)
    return [PostgresMockFactory.track_lyrics(id=id_) for id_ in tracks_ids]


@fixture(scope="class")
def audio_features(spotify_tracks: List[SpotifyTrack]) -> List[AudioFeatures]:
    tracks_ids = _sample_spotify_ids(spotify_tracks)
    return [PostgresMockFactory.audio_features(id=id_) for id_ in tracks_ids]


def _sample_spotify_ids(orms: List[Union[SpotifyArtist, SpotifyTrack]]) -> List[str]:
    n_elements = randint(2, len(orms))
    records = sample(orms, k=n_elements)

    return [track.id for track in records]
