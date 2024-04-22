from base64 import b64encode
from io import BytesIO
from typing import List, Any, Dict, Optional
from urllib.parse import urlencode

import numpy as np
from PIL import Image
from _pytest.logging import LogCaptureFixture
from genie_common.utils import random_alphanumeric_string
from spotipyio import SpotifySearchType

from server.consts.api_consts import ID
from server.consts.app_consts import MESSAGE
from server.consts.data_consts import URI, ARTISTS, ITEMS, NAME
from server.consts.openai_consts import CONTENT, CHOICES
from server.utils.spotify_utils import to_uris


def random_image_bytes(width: int = 1024, height: int = 1024, mode: str = "RGB", format_: str = "PNG") -> bytes:
    random_pixels = np.random.randint(255, size=(height, width, 3), dtype=np.uint8)
    image = Image.fromarray(random_pixels, mode=mode)
    image_bytes = BytesIO()
    image.save(image_bytes, format=format_)

    return image_bytes.getvalue()


def random_encoded_image() -> str:
    image = random_image_bytes()
    return b64encode(image).decode("utf-8")


def random_playlist_item(uri: str) -> Dict[str, str]:
    return {URI: uri}


def build_spotify_url(routes: List[str], params: Optional[Dict[str, Any]] = None) -> str:
    url = "https://api.spotify.com/v1"

    for route in routes:
        url += f'/{route.strip("/")}'

    if params is not None:
        return f"{url}?{urlencode(params)}"

    return url


def random_track_uri() -> str:
    track_id = random_alphanumeric_string(min_length=32, max_length=32)
    uris = to_uris(SpotifySearchType.TRACK, track_id)

    return uris[0]


def assert_expected_level_logs_count(caplog: LogCaptureFixture, level: str, expected: int) -> None:
    level_records = [record for record in caplog.records if record.levelname == level]
    assert len(level_records) == expected


def build_chat_completions_response(content: str) -> dict:
    return {
        CHOICES: [
            {
                MESSAGE: {
                    CONTENT: content
                }
            }
        ]
    }


def build_artists_search_response(artist_id: str, artist_name: str) -> dict:
    return {
        ARTISTS: {
            ITEMS: [
                {ID: artist_id, NAME: artist_name}
            ]
        }
    }
