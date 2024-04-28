from random import randint, choice
from typing import List

import pandas as pd
from _pytest.fixtures import fixture
from genie_common.utils import random_string_array, random_alphanumeric_string, random_enum_value, random_boolean, \
    random_datetime
from genie_datastores.postgres.models import SpotifyAlbumType
from genie_datastores.postgres.testing import PostgresMockFactory
from pandas import DataFrame
from pandas._testing import assert_frame_equal

from server.data.track_features import TrackFeatures
from server.logic.playlist_imitation.playlist_details_serializer import PlaylistDetailsSerializer
from tests.server.utils import random_spotify_id


class TestPlaylistDetailsSerializer:
    def test_serialize(self, serializer: PlaylistDetailsSerializer, tracks_features: List[TrackFeatures], expected: DataFrame):
        actual = serializer.serialize(tracks_features)
        assert_frame_equal(actual, expected)

    @fixture(scope="class")
    def serializer(self) -> PlaylistDetailsSerializer:
        return PlaylistDetailsSerializer()

    @fixture(scope="class")
    def tracks_features(self) -> List[TrackFeatures]:
        tracks_number = randint(1, 10)
        return [self._random_track_features() for _ in range(tracks_number)]

    @fixture(scope="class")
    def expected(self, tracks_features: List[TrackFeatures]) -> DataFrame:
        records = [self._to_record(track) for track in tracks_features]
        return pd.DataFrame.from_records(records)

    def _random_track_features(self) -> TrackFeatures:
        return TrackFeatures(
            track=self._random_track_response(),
            artist=self._random_artist_response(),
            audio=self._random_audio_features_response()
        )

    @staticmethod
    def _to_record(track_features: TrackFeatures) -> dict:
        return {
            'acousticness': track_features.audio['acousticness'],
            'danceability': track_features.audio['danceability'],
            'duration_ms': track_features.audio['duration_ms'],
            'energy': track_features.audio['energy'],
            'instrumentalness': track_features.audio['instrumentalness'],
            'key': track_features.audio['key'],
            'liveness': track_features.audio['liveness'],
            'loudness': track_features.audio['loudness'],
            'mode': track_features.audio['mode'],
            'speechiness': track_features.audio['speechiness'],
            'tempo': track_features.audio['tempo'],
            'time_signature': track_features.audio['time_signature'],
            'valence': track_features.audio['valence'],
            'total_tracks': track_features.track['album']['total_tracks'],
            'album_name': track_features.track['album']['name'],
            'release_date': track_features.track['album']['release_date'],
            'disc_number': track_features.track['disc_number'],
            'explicit': track_features.track['explicit'],
            'name': track_features.track['name'],
            'popularity': track_features.track['popularity'],
            'track_number': track_features.track['track_number'],
            'uri': track_features.track['uri'],
            'artist_followers': track_features.artist['followers']['total'],
            'genres': track_features.artist['genres'],
            'artist_name': track_features.artist['name'],
            'artist_popularity': track_features.artist['popularity']
        }

    @staticmethod
    def _random_audio_features_response() -> dict:
        orm = PostgresMockFactory.audio_features()
        audio_features = orm.to_dict()
        additional_response_fields = {
            "analysis_url": f"https://api.spotify.com/v1/audio-analysis/{orm.id}",
            "track_href": f"https://api.spotify.com/v1/tracks/{orm.id}",
            "type": "audio_features",
            "uri": f"spotify:track:{orm.id}",
        }
        audio_features.update(additional_response_fields)

        return audio_features

    @staticmethod
    def _random_artist_response() -> dict:
        artist_id = random_spotify_id()
        return {
            "external_urls": {
                "spotify": f"https://open.spotify.com/artist/{artist_id}"
            },
            "followers": {
                "href": None,
                "total": 10239890
            },
            "genres": random_string_array(),
            "href": f"https://api.spotify.com/v1/artists/{artist_id}",
            "id": artist_id,
            "images": [],
            "name": random_alphanumeric_string(),
            "popularity": randint(0, 100),
            "type": "artist",
            "uri": f"spotify:artist:{artist_id}"
        }

    @staticmethod
    def _random_track_response() -> dict:
        album_id = random_spotify_id()
        artist_id = random_spotify_id()
        artist_name = random_alphanumeric_string()
        track_id = random_spotify_id()

        return {
            "album": {
                "album_type": random_enum_value(SpotifyAlbumType).value,
                "total_tracks": randint(1, 15),
                "available_markets": random_string_array(),
                "external_urls": {
                    "spotify": f"https://open.spotify.com/album/{album_id}"
                },
                "href": f"https://api.spotify.com/v1/albums/{album_id}",
                "id": album_id,
                "images": [],
                "name": random_spotify_id(),
                "release_date": random_datetime().strftime("%Y-%m-%d"),
                "release_date_precision": choice(["day", "month", "year"]),
                "type": "album",
                "uri": f"spotify:album:{album_id}",
                "artists": [
                    {
                        "external_urls": {
                            "spotify": f"https://open.spotify.com/artist/{artist_id}"
                        },
                        "href": f"https://api.spotify.com/v1/artists/{artist_id}",
                        "id": artist_id,
                        "name": artist_name,
                        "type": "artist",
                        "uri": f"spotify:artist:{artist_id}"
                    }
                ]
            },
            "artists": [
                {
                    "external_urls": {
                        "spotify": f"https://open.spotify.com/artist/{artist_id}"
                    },
                    "href": f"https://api.spotify.com/v1/artists/{artist_id}",
                    "id": artist_id,
                    "name": artist_name,
                    "type": "artist",
                    "uri": f"spotify:artist:{artist_id}"
                }
            ],
            "available_markets": random_string_array(),
            "disc_number": randint(1, 3),
            "duration_ms": 207959,
            "explicit": random_boolean(),
            "external_ids": {
                "isrc": random_alphanumeric_string()
            },
            "external_urls": {
                "spotify": f"https://open.spotify.com/track/{track_id}"
            },
            "href": f"https://api.spotify.com/v1/tracks/{track_id}",
            "id": track_id,
            "name": random_alphanumeric_string(),
            "popularity": randint(0, 100),
            "preview_url": random_alphanumeric_string(),
            "track_number": randint(1, 15),
            "type": "track",
            "uri": f"spotify:track:{track_id}",
            "is_local": random_boolean()
        }
