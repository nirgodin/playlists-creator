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

    def __post_init__(self):
        self.access_token_generator_response = AccessTokenGenerator.generate(
            grant_type=self.grant_type,
            access_code=self.access_code
        )
        self.headers = self._build_request_headers()

    def _build_request_headers(self) -> Optional[Dict[str, str]]:
        bearer_token = self.access_token_generator_response.get(ACCESS_TOKEN)

        if bearer_token is None:
            return

        return build_spotify_headers(bearer_token)
