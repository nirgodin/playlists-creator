from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json
from spotipyio import SpotifyClient


@dataclass_json
@dataclass
class PlaylistCreationConfig:
    spotify_client: SpotifyClient
    playlist_details: dict
    uris: List[str]
