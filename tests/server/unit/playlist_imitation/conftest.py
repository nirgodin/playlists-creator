from random import randint, choice
from typing import List

from _pytest.fixtures import fixture
from genie_common.utils import random_string_array, random_alphanumeric_string, random_enum_value, random_boolean, \
    random_datetime
from genie_datastores.postgres.models import SpotifyAlbumType
from genie_datastores.testing.postgres import PostgresMockFactory

from server.data.track_features import TrackFeatures
from tests.server.utils import random_spotify_id


@fixture(scope="class")
def tracks_features() -> List[TrackFeatures]:
    tracks_number = randint(1, 10)
    return [_random_track_features() for _ in range(tracks_number)]


def _random_track_features() -> TrackFeatures:
    return TrackFeatures(
        track=_random_track_response(),
        artist=_random_artist_response(),
        audio=_random_audio_features_response()
    )


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
