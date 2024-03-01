from typing import Optional

from genie_common.models.openai import ImageSize
from genie_common.openai import OpenAIClient
from spotipyio import SpotifyClient

from server.consts.app_consts import PLAYLIST_DETAILS, EXISTING_PLAYLIST
from server.consts.data_consts import TRACK
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.playlist_resources import PlaylistResources
from server.logic.cases_manager import CasesManager
from server.logic.data_collection.spotify_playlist_details_collector import PlaylistDetailsCollector
from server.data.playlist_imitation.playlist_details import PlaylistDetails
from server.logic.playlist_imitation.playlist_imitator import PlaylistImitator
from server.logic.playlists_creator import PlaylistsCreator
from server.tools.authenticator import Authenticator
from server.tools.case_progress_reporter import CaseProgressReporter
from server.tools.spotify_session_creator import SpotifySessionCreator
from server.utils.spotify_utils import extract_tracks_from_response


class ExistingPlaylistController(BaseContentController):
    def __init__(self,
                 playlists_creator: PlaylistsCreator,
                 openai_client: OpenAIClient,
                 session_creator: SpotifySessionCreator,
                 playlists_imitator: PlaylistImitator,
                 case_progress_reporter: CaseProgressReporter,
                 cases_manager: CasesManager,
                 playlist_details_collector: PlaylistDetailsCollector):
        super().__init__(
            playlists_creator=playlists_creator,
            openai_client=openai_client,
            session_creator=session_creator,
            case_progress_reporter=case_progress_reporter,
            cases_manager=cases_manager
        )
        self._playlist_imitator = playlists_imitator
        self._playlist_details_collector = playlist_details_collector

    async def _generate_playlist_resources(self,
                                           case_id: str,
                                           request_body: dict,
                                           dir_path: str,
                                           spotify_client: SpotifyClient) -> PlaylistResources:
        existing_playlist_url = request_body[PLAYLIST_DETAILS][EXISTING_PLAYLIST]
        playlist_details = await self._extract_raw_playlist_details(
            case_id=case_id,
            playlist_url=existing_playlist_url,
            spotify_client=spotify_client
        )

        if playlist_details is None:
            return PlaylistResources(None, None)

        return await self._playlist_imitator.imitate_playlist(playlist_details, dir_path)

    async def _generate_playlist_cover(self, request_body: dict, image_path: str) -> Optional[str]:
        return await self._openai_client.images_variation.collect(
            image=open(image_path, 'rb'),
            n=1,
            size=ImageSize.P512
        )

    async def _extract_raw_playlist_details(self,
                                            case_id: str,
                                            playlist_url: str,
                                            spotify_client: SpotifyClient) -> Optional[PlaylistDetails]:
        playlist_id = self._extract_playlist_id_from_url(playlist_url)
        playlist = await spotify_client.playlists.info.run_single(playlist_id)
        items = extract_tracks_from_response(playlist)
        tracks = [track.get(TRACK) for track in items]

        return await self._playlist_details_collector.collect_playlist(
            case_id=case_id,
            tracks=tracks,
            spotify_client=spotify_client
        )

    @staticmethod
    def _extract_playlist_id_from_url(playlist_url: str) -> str:
        split_url = playlist_url.split('/')
        last_url_component = split_url[-1]
        split_url_params = last_url_component.split('?')

        return split_url_params[0]
