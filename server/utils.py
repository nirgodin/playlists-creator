from typing import Iterable, Dict

from server.access_token_generator import AccessTokenGenerator
from server.spotify_scope import SpotifyScope


def build_spotify_headers(is_authorization_token: bool = False, scopes: Iterable[SpotifyScope] = ()) -> Dict[str, str]:
    bearer_token = AccessTokenGenerator.generate(is_authorization_token, scopes)
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }
