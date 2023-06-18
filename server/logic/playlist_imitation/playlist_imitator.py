from typing import List, Optional

from server.logic.data_collection.spotify_playlist_details_collector import PlaylistDetailsCollector
from server.logic.playlist_imitation.playlist_details_pipeline import PlaylistDetailsPipeline
from server.logic.playlist_imitation.playlist_details_serializer import PlaylistDetailsSerializer
from server.logic.playlist_imitation.playlist_imitator_tracks_selector import PlaylistImitatorTracksSelector


class PlaylistImitator:
    def __init__(self):
        self._playlist_details_serializer = PlaylistDetailsSerializer()
        self._tracks_selector = PlaylistImitatorTracksSelector()
        self._transformation_pipeline = PlaylistDetailsPipeline(is_training=False)

    async def imitate_playlist(self, playlist_url: str) -> Optional[List[str]]:
        playlist_id = self._extract_playlist_id_from_url(playlist_url)

        async with PlaylistDetailsCollector() as playlist_details_collector:
            raw_playlist_details = await playlist_details_collector.collect_playlist(playlist_id)

        if raw_playlist_details is None:
            return

        serialized_playlist_data = self._playlist_details_serializer.serialize(raw_playlist_details)
        transformed_playlist_data = self._transformation_pipeline.transform(serialized_playlist_data)

        return self._tracks_selector.select_tracks(transformed_playlist_data)

    @staticmethod
    def _extract_playlist_id_from_url(playlist_url: str) -> str:
        split_url = playlist_url.split('/')
        last_url_component = split_url[-1]
        split_url_params = last_url_component.split('?')

        return split_url_params[0]
