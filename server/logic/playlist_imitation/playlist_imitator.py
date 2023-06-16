import asyncio

from aiohttp import ClientSession

from server.logic.data_collection.spotify_playlist_details_collector import PlaylistDetailsCollector
from server.logic.playlist_imitation.playlist_details_serializer import PlaylistDetailsSerializer
from server.logic.playlist_imitation.playlist_imitator_tracks_selector import PlaylistImitatorTracksSelector
from server.utils.general_utils import build_spotify_client_credentials_headers


class PlaylistImitator:
    def __init__(self, session: ClientSession):
        self._playlist_details_collector = PlaylistDetailsCollector(session)
        self._playlist_details_serializer = PlaylistDetailsSerializer()
        self._tracks_selector = PlaylistImitatorTracksSelector()

    async def imitate_playlist(self, playlist_id: str):
        raw_playlist_details = await self._playlist_details_collector.collect_playlist(playlist_id)
        serialized_playlist_details = self._playlist_details_serializer.serialize(raw_playlist_details)
        tracks_uris = self._tracks_selector.select_tracks(serialized_playlist_details)


if __name__ == '__main__':
    PLAYLIST_ID = '7rWJ3kaE2N7pmKLtLAHENL'

    headers = build_spotify_client_credentials_headers()
    session = ClientSession(headers=headers)
    imitator = PlaylistImitator(session)
    asyncio.get_event_loop().run_until_complete(imitator.imitate_playlist(PLAYLIST_ID))
