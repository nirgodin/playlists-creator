import os
from contextlib import asynccontextmanager

from spotipyio import SpotifyClient
from spotipyio.logic.authentication.spotify_grant_type import SpotifyGrantType
from spotipyio.logic.authentication.spotify_session import SpotifySession

from server.consts.api_consts import MAX_SPOTIFY_PLAYLIST_SIZE
from server.consts.app_consts import ACCESS_CODE
from server.consts.data_consts import ITEMS, TRACKS
from server.consts.env_consts import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
from server.utils.general_utils import sample_list


def extract_tracks_from_response(playlist: dict) -> list:
    return playlist.get(TRACKS, {}).get(ITEMS, [])


def sample_uris(uris: list, n_selected_candidates: int = MAX_SPOTIFY_PLAYLIST_SIZE) -> list:
    n_candidates = len(uris)
    uris_indexes = sample_list(n_candidates, n_selected_candidates)

    return [uris[i] for i in uris_indexes]


@asynccontextmanager
async def build_spotify_client(request_body: dict) -> SpotifyClient:
    session = None

    try:
        access_code = request_body[ACCESS_CODE]
        raw_session = SpotifySession(
            client_id=os.environ[SPOTIPY_CLIENT_ID],
            client_secret=os.environ[SPOTIPY_CLIENT_SECRET],
            redirect_uri=os.environ[SPOTIPY_REDIRECT_URI],
            grant_type=SpotifyGrantType.AUTHORIZATION_CODE,
            access_code=access_code
        )
        session = await raw_session.__aenter__()

        yield SpotifyClient.create(session)

    finally:
        if session is not None:
            await session.__aexit__("", "", "")
