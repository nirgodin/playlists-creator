from spotipyio import SpotifyClient

from server.consts.app_consts import ACCESS_CODE
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.playlist_resources import PlaylistResources
from server.logic.data_collection.wrapped_tracks_collector import WrappedTracksCollector
from server.logic.openai.openai_client import OpenAIClient
from server.logic.playlists_creator import PlaylistsCreator


class WrappedController(BaseContentController):
    def __init__(self,
                 playlists_creator: PlaylistsCreator,
                 openai_client: OpenAIClient,
                 wrapped_tracks_collector: WrappedTracksCollector):
        super().__init__(playlists_creator, openai_client)
        self._wrapped_tracks_collector = wrapped_tracks_collector

    async def _generate_playlist_resources(self,
                                           request_body: dict,
                                           dir_path: str,
                                           spotify_client: SpotifyClient) -> PlaylistResources:
        access_code = request_body[ACCESS_CODE]
        uris = await self._wrapped_tracks_collector.collect(access_code)
        return PlaylistResources(uris=uris, cover_image_path=None)

    async def _generate_playlist_cover(self, request_body: dict, image_path: str) -> None:
        raise NotImplementedError
