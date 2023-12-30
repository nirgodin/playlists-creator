from typing import List

from genie_common.utils import safe_nested_get
from spotipyio.logic.collectors.search_collectors.spotify_search_type import SpotifySearchType

from server.consts.api_consts import MAX_SPOTIFY_PLAYLIST_SIZE
from server.consts.data_consts import ITEMS, TRACKS
from server.utils.general_utils import sample_list


def extract_tracks_from_response(playlist: dict) -> list:
    return safe_nested_get(playlist, [TRACKS, ITEMS], default=[])


def sample_uris(uris: list, n_selected_candidates: int = MAX_SPOTIFY_PLAYLIST_SIZE) -> list:
    n_candidates = len(uris)
    uris_indexes = sample_list(n_candidates, n_selected_candidates)

    return [uris[i] for i in uris_indexes]


def to_uris(spotify_type: SpotifySearchType, *spotify_id: str) -> List[str]:
    return [f"spotify:{spotify_type.value}:{id_}" for id_ in spotify_id]
