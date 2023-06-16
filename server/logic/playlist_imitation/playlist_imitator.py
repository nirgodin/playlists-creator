from typing import List

from server.logic.data_collection.spotify_playlist_details_collector import PlaylistDetailsCollector
from server.logic.playlist_imitation.playlist_details_serializer import PlaylistDetailsSerializer
from server.logic.playlist_imitation.playlist_imitator_tracks_selector import PlaylistImitatorTracksSelector


class PlaylistImitator:
    def __init__(self):
        self._playlist_details_collector = PlaylistDetailsCollector()
        self._playlist_details_serializer = PlaylistDetailsSerializer()
        self._tracks_selector = PlaylistImitatorTracksSelector()

    async def imitate_playlist(self, playlist_id: str) -> List[str]:
        raw_playlist_details = await self._playlist_details_collector.collect_playlist(playlist_id)
        serialized_playlist_details = self._playlist_details_serializer.serialize(raw_playlist_details)

        return self._tracks_selector.select_tracks(serialized_playlist_details)
