from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json

from server.data.spotify_grant_type import SpotifyGrantType


@dataclass_json
@dataclass
class PlaylistCreationConfig:
    access_code: str
    playlist_details: dict
    grant_type: SpotifyGrantType
    uris: List[str]
