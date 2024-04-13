from typing import Optional, List, Dict

from genie_common.tools import logger
from spotipyio import SpotifyClient

from server.consts.app_consts import PHOTO
from server.consts.data_consts import TRACKS, URI
from server.consts.prompt_consts import PHOTO_ARTISTS_PROMPT_PREFIX
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.case_status import CaseStatus
from server.data.chat_completions_request import ChatCompletionsRequest
from server.data.playlist_creation_context import PlaylistCreationContext
from server.data.playlist_resources import PlaylistResources
from server.logic.ocr.artists_searcher import ArtistsSearcher
from server.logic.ocr.image_text_extractor import ImageTextExtractor
from server.logic.openai.openai_adapter import OpenAIAdapter
from server.utils.general_utils import build_prompt
from server.utils.image_utils import current_timestamp_image_path, save_image_from_bytes
from server.utils.spotify_utils import sample_uris


class PhotoController(BaseContentController):
    def __init__(self,
                 context: PlaylistCreationContext,
                 image_text_extractor: ImageTextExtractor,
                 openai_adapter: OpenAIAdapter,
                 artists_searcher: ArtistsSearcher):
        super().__init__(context)
        self._image_text_extractor = image_text_extractor
        self._openai_adapter = openai_adapter
        self._artists_searcher = artists_searcher

    async def _generate_playlist_resources(self,
                                           case_id: str,
                                           request_body: dict,
                                           dir_path: str,
                                           spotify_client: SpotifyClient) -> PlaylistResources:
        cover_image_path = self._save_photo(request_body[PHOTO], dir_path)

        async with self._context.case_progress_reporter.report(case_id, CaseStatus.PHOTO):
            photo_text = self._image_text_extractor.extract(cover_image_path)

        async with self._context.case_progress_reporter.report(case_id, CaseStatus.PROMPT):
            artists = await self._extract_artists_names(photo_text)

        async with self._context.case_progress_reporter.report(case_id, CaseStatus.TRACKS):
            uris = await self._generate_tracks_uris(artists, spotify_client)
            return PlaylistResources(
                uris=sample_uris(uris),
                cover_image_path=cover_image_path
            )

    @staticmethod
    def _save_photo(photo: bytes, dir_path: str) -> str:
        image_path = current_timestamp_image_path(dir_path)
        save_image_from_bytes(photo, image_path)

        return image_path

    async def _extract_artists_names(self, photo_text: str) -> Optional[List[str]]:
        logger.info("Extracting artists names from provided photo")
        prompt_suffix = f'```\n{photo_text}\n```'
        prompt = build_prompt(PHOTO_ARTISTS_PROMPT_PREFIX, prompt_suffix)
        request = ChatCompletionsRequest(
            prompt=prompt,
            expected_type=list
        )

        return await self._openai_adapter.chat_completions(request)

    async def _generate_tracks_uris(self,
                                    artists: List[str],
                                    spotify_client: SpotifyClient,
                                    country: str = "US") -> Optional[List[str]]:
        if artists is None:
            return

        artists_ids = await self._artists_searcher.search(artists, spotify_client)
        if artists_ids:
            top_tracks = await spotify_client.artists.top_tracks.run(artists_ids, market=country)
            return self._extract_tracks_uris(top_tracks)

    @staticmethod
    def _extract_tracks_uris(tracks: List[Dict[str, List[dict]]]) -> List[str]:
        uris = []

        for artist_tracks in tracks:
            inner_tracks = artist_tracks.get(TRACKS, [])

            if inner_tracks:
                for track in inner_tracks:
                    uris.append(track[URI])

        return sample_uris(uris)

    async def _generate_playlist_cover(self, request_body: dict, image_path: str) -> Optional[str]:
        return image_path
