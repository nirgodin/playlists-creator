import os.path
from typing import List, Optional

from pandas import DataFrame

from server.consts.data_consts import SONG, ARTIST_NAME, NAME
from server.data.playlist_resources import PlaylistResources
from server.logic.data_collection.spotify_playlist_details_collector import PlaylistDetailsCollector
from server.logic.playlist_imitation.playlist_details import PlaylistDetails
from server.logic.playlist_imitation.playlist_details_pipeline import PlaylistDetailsPipeline
from server.logic.playlist_imitation.playlist_details_serializer import PlaylistDetailsSerializer
from server.logic.playlist_imitation.playlist_imitator_tracks_selector import PlaylistImitatorTracksSelector
from server.utils.datetime_utils import get_current_timestamp
from server.utils.image_utils import save_image_from_url


class PlaylistImitator:
    def __init__(self):
        self._playlist_details_serializer = PlaylistDetailsSerializer()
        self._tracks_selector = PlaylistImitatorTracksSelector()
        self._transformation_pipeline = PlaylistDetailsPipeline(is_training=False)

    async def imitate_playlist(self, playlist_url: str, dir_path: str) -> PlaylistResources:
        raw_playlist_details = await self._extract_raw_playlist_details(playlist_url)
        if raw_playlist_details is None:
            return PlaylistResources(None, None)

        transformed_playlist_data = self._transform_playlist_data(raw_playlist_details)
        tracks_uris = self._tracks_selector.select_tracks(transformed_playlist_data)
        cover_image_path = self._save_original_cover_image(dir_path, raw_playlist_details.cover_image_url)

        return PlaylistResources(
            uris=tracks_uris,
            cover_image_path=cover_image_path
        )

    async def _extract_raw_playlist_details(self, playlist_url: str) -> PlaylistDetails:
        playlist_id = self._extract_playlist_id_from_url(playlist_url)

        async with PlaylistDetailsCollector() as playlist_details_collector:
            return await playlist_details_collector.collect_playlist(playlist_id)

    @staticmethod
    def _extract_playlist_id_from_url(playlist_url: str) -> str:
        split_url = playlist_url.split('/')
        last_url_component = split_url[-1]
        split_url_params = last_url_component.split('?')

        return split_url_params[0]

    def _transform_playlist_data(self, raw_playlist_details: PlaylistDetails) -> DataFrame:
        serialized_playlist_data = self._playlist_details_serializer.serialize(raw_playlist_details)
        serialized_playlist_data[SONG] = serialized_playlist_data[ARTIST_NAME] + ' - ' + serialized_playlist_data[NAME]

        return self._transformation_pipeline.transform(serialized_playlist_data)

    @staticmethod
    def _save_original_cover_image(dir_path: str, cover_image_url: str) -> str:
        timestamp = get_current_timestamp()
        file_name = f'{timestamp}.png'
        image_path = os.path.join(dir_path, file_name)
        save_image_from_url(cover_image_url, image_path)

        return image_path
