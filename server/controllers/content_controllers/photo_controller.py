from typing import Optional

from genie_common.openai import OpenAIClient
from spotipyio import SpotifyClient

from server.consts.app_consts import PHOTO
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.playlist_resources import PlaylistResources
from server.logic.ocr.tracks_uris_image_extractor import TracksURIsImageExtractor
from server.logic.playlists_creator import PlaylistsCreator
from server.tools.authenticator import Authenticator
from server.tools.case_progress_reporter import CaseProgressReporter
from server.tools.spotify_session_creator import SpotifySessionCreator
from server.utils.image_utils import current_timestamp_image_path, save_image_from_bytes
from server.utils.spotify_utils import sample_uris


class PhotoController(BaseContentController):
    def __init__(self,
                 playlists_creator: PlaylistsCreator,
                 openai_client: OpenAIClient,
                 session_creator: SpotifySessionCreator,
                 tracks_uris_extractor: TracksURIsImageExtractor,
                 case_progress_reporter: CaseProgressReporter):
        super().__init__(
            playlists_creator=playlists_creator,
            openai_client=openai_client,
            session_creator=session_creator,
            case_progress_reporter=case_progress_reporter
        )
        self._tracks_uris_extractor = tracks_uris_extractor

    async def _generate_playlist_resources(self,
                                           case_id: str,
                                           request_body: dict,
                                           dir_path: str,
                                           spotify_client: SpotifyClient) -> PlaylistResources:
        cover_image_path = self._save_photo(request_body[PHOTO], dir_path)
        uris = await self._tracks_uris_extractor.extract_tracks_uris(
            case_id=case_id,
            image_path=cover_image_path,
            spotify_client=spotify_client
        )

        if uris is None:
            return PlaylistResources(None, None)

        return PlaylistResources(
            uris=sample_uris(uris),
            cover_image_path=cover_image_path
        )

    @staticmethod
    def _save_photo(photo: bytes, dir_path: str) -> str:
        image_path = current_timestamp_image_path(dir_path)
        save_image_from_bytes(photo, image_path)

        return image_path

    async def _generate_playlist_cover(self, request_body: dict, image_path: str) -> Optional[str]:
        return image_path
