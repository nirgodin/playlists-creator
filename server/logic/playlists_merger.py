from random import shuffle
from typing import List

from genie_common.utils import safe_nested_get, chain_lists
from spotipyio import SpotifyClient

from server.consts.data_consts import ITEMS, TRACKS, URI, TRACK


class PlaylistsMerger:
    @staticmethod
    async def merge(spotify_client: SpotifyClient, ids: List[str], shuffle_items: bool = False) -> List[str]:
        playlists = await spotify_client.playlists.info.run(ids)
        uris: List[List[str]] = [PlaylistsMerger._extract_playlist_uris(playlist) for playlist in playlists]
        flattened_uris = chain_lists(uris)

        if shuffle_items:
            shuffle(flattened_uris)

        return flattened_uris

    @staticmethod
    def _extract_playlist_uris(playlist: dict) -> List[str]:
        items = safe_nested_get(playlist, [TRACKS, ITEMS], default=[])
        uris = []

        for item in items:
            uri = safe_nested_get(item, [TRACK, URI])

            if uri is not None:
                uris.append(uri)

        return uris
