from aiohttp import ClientSession
from pandas import DataFrame

from server.consts.data_consts import SONG, ARTIST_NAME, NAME
from server.data.playlist_resources import PlaylistResources
from server.data.playlist_imitation.playlist_details import PlaylistDetails
from server.logic.playlist_imitation.playlist_details_pipeline import PlaylistDetailsPipeline
from server.logic.playlist_imitation.playlist_details_serializer import PlaylistDetailsSerializer
from server.logic.playlist_imitation.playlist_imitator_tracks_selector import PlaylistImitatorTracksSelector
from server.utils.image_utils import save_image_from_url, current_timestamp_image_path


class PlaylistImitator:
    def __init__(self,
                 session: ClientSession,
                 playlist_details_serializer: PlaylistDetailsSerializer = PlaylistDetailsSerializer(),
                 tracks_selector: PlaylistImitatorTracksSelector = PlaylistImitatorTracksSelector(),
                 transformation_pipeline: PlaylistDetailsPipeline = PlaylistDetailsPipeline(is_training=False)):
        self._session = session
        self._playlist_details_serializer = playlist_details_serializer
        self._tracks_selector = tracks_selector
        self._transformation_pipeline = transformation_pipeline

    async def imitate_playlist(self, playlist_details: PlaylistDetails, dir_path: str) -> PlaylistResources:
        transformed_playlist_data = self._transform_playlist_data(playlist_details)
        tracks_uris = self._tracks_selector.select_tracks(transformed_playlist_data)
        # TODO: Think how to do this
        cover_image_path = None  # await self._save_original_cover_image(dir_path, playlist_details.cover_image_url)

        return PlaylistResources(
            uris=tracks_uris,
            cover_image_path=cover_image_path
        )

    def _transform_playlist_data(self, playlist_details: PlaylistDetails) -> DataFrame:
        serialized_playlist_data = self._playlist_details_serializer.serialize(playlist_details)
        serialized_playlist_data[SONG] = serialized_playlist_data[ARTIST_NAME] + ' - ' + serialized_playlist_data[NAME]

        return self._transformation_pipeline.transform(serialized_playlist_data)

    async def _save_original_cover_image(self, dir_path: str, cover_image_url: str) -> str:
        image_path = current_timestamp_image_path(dir_path)
        await save_image_from_url(self._session, cover_image_url, image_path)

        return image_path
