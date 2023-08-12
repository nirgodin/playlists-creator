from dataclasses import dataclass
from typing import List, Optional, Dict

from dataclasses_json import dataclass_json

from server.consts.api_consts import ACCESS_TOKEN
from server.data.spotify_grant_type import SpotifyGrantType
from server.logic.access_token_generator import AccessTokenGenerator
from server.utils.general_utils import build_spotify_headers


@dataclass_json
@dataclass
class PlaylistCreationConfig:
    access_code: str
    playlist_details: dict
    grant_type: SpotifyGrantType
    uris: List[str]
    access_token_generator_response: Optional[Dict[str, str]]
    headers: Optional[Dict[str, str]]
