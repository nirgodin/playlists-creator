from typing import Dict

from server.access_token_generator import AccessTokenGenerator


def build_spotify_headers(access_code: str) -> Dict[str, str]:
    bearer_token = AccessTokenGenerator.generate(access_code)
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }
