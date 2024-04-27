from spotipyio import SpotifyClient
from spotipyio.logic.collectors.top_items_collectors.items_type import ItemsType
from spotipyio.logic.collectors.top_items_collectors.time_range import TimeRange

from server.consts.data_consts import ITEMS
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.case_status import CaseStatus
from server.data.playlist_creation_context import PlaylistCreationContext
from server.data.playlist_resources import PlaylistResources
from server.logic.data_collection.spotify_playlist_details_collector import PlaylistDetailsCollector
from server.logic.playlist_imitation.playlist_imitator import PlaylistImitator


class ForYouController(BaseContentController):
    def __init__(self,
                 context: PlaylistCreationContext,
                 playlists_imitator: PlaylistImitator,
                 playlist_details_collector: PlaylistDetailsCollector):
        super().__init__(context)
        self._playlist_details_collector = playlist_details_collector
        self._playlists_imitator = playlists_imitator

    async def _generate_playlist_resources(self,
                                           case_id: str,
                                           request_body: dict,
                                           dir_path: str,
                                           spotify_client: SpotifyClient) -> PlaylistResources:
        response = await spotify_client.current_user.top_items.run(
            items_type=ItemsType.TRACKS,
            time_range=TimeRange.MEDIUM_TERM,
            limit=50
        )

        async with self._context.case_progress_reporter.report(case_id=case_id, status=CaseStatus.PLAYLIST_DETAILS):
            playlist_details = await self._playlist_details_collector.collect_playlist(
                tracks=response[ITEMS],
                spotify_client=spotify_client
            )

        async with self._context.case_progress_reporter.report(case_id=case_id, status=CaseStatus.TRACKS):
            return await self._playlists_imitator.imitate_playlist(
                case_id=case_id,
                playlist_details=playlist_details,
                dir_path=dir_path
            )

    async def _generate_playlist_cover(self, request_body: dict, image_path: str) -> None:  # TODO: Implement
        raise NotImplementedError
