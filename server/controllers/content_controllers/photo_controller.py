import json
from typing import Optional

from werkzeug.datastructures import FileStorage

from server.consts.api_consts import MAX_SPOTIFY_PLAYLIST_SIZE
from server.consts.app_consts import REQUEST_BODY, PHOTO
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.playlist_resources import PlaylistResources
from server.logic.access_token_generator import AccessTokenGenerator
from server.logic.ocr.tracks_uris_image_extractor import TracksURIsImageExtractor
from server.logic.openai.openai_client import OpenAIClient
from server.logic.playlist_cover_photo_creator import PlaylistCoverPhotoCreator
from server.logic.playlists_creator import PlaylistsCreator
from server.utils.general_utils import sample_list
from server.utils.image_utils import current_timestamp_image_path


class PhotoController(BaseContentController):
    def __init__(self,
                 playlists_creator: PlaylistsCreator,
                 playlists_cover_photo_creator: PlaylistCoverPhotoCreator,
                 openai_client: OpenAIClient,
                 access_token_generator: AccessTokenGenerator,
                 tracks_uris_extractor: TracksURIsImageExtractor):
        super().__init__(playlists_creator, playlists_cover_photo_creator, openai_client, access_token_generator)
        self._tracks_uris_extractor = tracks_uris_extractor

    def _get_request_body(self, request: dict) -> dict:
        body = request.files[REQUEST_BODY]
        data = body.read()
        request_body = json.loads(data)
        request_body[PHOTO] = request.files[PHOTO]

        return request_body

    async def _generate_playlist_resources(self, request_body: dict, dir_path: str) -> PlaylistResources:
        cover_image_path = self._save_photo(request_body[PHOTO], dir_path)
        uris = await self._tracks_uris_extractor.extract_tracks_uris(cover_image_path)

        if uris is None:
            return PlaylistResources(None, None)

        n_candidates = len(uris)
        selected_uris_indexes = sample_list(n_candidates, MAX_SPOTIFY_PLAYLIST_SIZE)
        tracks_uris = [uris[i] for i in selected_uris_indexes]

        return PlaylistResources(
            uris=tracks_uris,
            cover_image_path=cover_image_path
        )

    @staticmethod
    def _save_photo(photo: FileStorage, dir_path: str) -> str:
        image_path = current_timestamp_image_path(dir_path)
        photo.save(image_path)

        return image_path

    async def _generate_playlist_cover(self, request_body: dict, image_path: str) -> Optional[str]:
        return image_path
