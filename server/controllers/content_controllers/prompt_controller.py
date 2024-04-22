from base64 import b64decode
from typing import List, Optional, Union

from genie_common.models.openai import ImageSize, DallEModel
from genie_common.tools.logs import logger
from spotipyio import SpotifyClient

from server.consts.api_consts import MAX_SPOTIFY_PLAYLIST_SIZE
from server.consts.app_consts import PLAYLIST_DETAILS, PROMPT
from server.consts.data_consts import URI
from server.consts.typing_consts import DataClass
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.case_status import CaseStatus
from server.data.playlist_creation_context import PlaylistCreationContext
from server.data.playlist_resources import PlaylistResources
from server.data.prompt_details import PromptDetails
from server.data.track_details import TrackDetails
from server.logic.prompt.prompt_serialization_manager import PromptSerializationManager
from server.logic.prompt_details_tracks_selector import PromptDetailsTracksSelector
from server.utils.image_utils import current_timestamp_image_path, save_image_from_bytes


class PromptController(BaseContentController):
    def __init__(self,
                 context: PlaylistCreationContext,
                 serialization_manager: PromptSerializationManager,
                 prompt_details_tracks_selector: PromptDetailsTracksSelector):
        super().__init__(context)
        self._serialization_manager = serialization_manager
        self._prompt_details_tracks_selector = prompt_details_tracks_selector

    async def _generate_playlist_resources(self,
                                           case_id: str,
                                           request_body: dict,
                                           dir_path: str,
                                           spotify_client: SpotifyClient) -> PlaylistResources:
        serialized_prompt = await self._serialize_prompt(request_body, case_id)

        async with self._context.case_progress_reporter.report(case_id, CaseStatus.TRACKS):
            tracks_uris = await self._to_uris(serialized_prompt, spotify_client)

        return PlaylistResources(
            uris=tracks_uris,
            cover_image_path=current_timestamp_image_path(dir_path)
        )

    async def _generate_playlist_cover(self, request_body: dict, image_path: str) -> Optional[str]:
        user_text = self._extract_user_text(request_body)
        playlist_cover_prompt = f'{user_text}, digital art'
        encoded_image: str = await self._context.openai_client.images_generation.collect(
            prompt=playlist_cover_prompt,
            model=DallEModel.DALLE_3,
            n=1,
            size=ImageSize.P1024
        )
        image: bytes = b64decode(encoded_image)
        save_image_from_bytes(image, image_path)

        return image_path

    async def _serialize_prompt(self, request_body: dict, case_id: str) -> Optional[DataClass]:
        logger.info("Serializing user text to known data model")
        user_text = self._extract_user_text(request_body)

        async with self._context.case_progress_reporter.report(case_id, CaseStatus.PROMPT):
            return await self._serialization_manager.serialize(user_text)

    async def _to_uris(self,
                       serialized_prompt: Optional[Union[PromptDetails, List[TrackDetails]]],
                       spotify_client: SpotifyClient) -> Optional[List[str]]:
        if isinstance(serialized_prompt, PromptDetails):
            return await self._prompt_details_tracks_selector.select_tracks(serialized_prompt)

        if isinstance(serialized_prompt, list):
            return await self._search_matching_tracks(serialized_prompt, spotify_client)

        logger.info("Prompt was not serialized to any relevant model. Returning None instead")

    @staticmethod
    async def _search_matching_tracks(tracks_details: List[TrackDetails], spotify_client: SpotifyClient) -> List[str]:
        search_items = [details.to_search_item() for details in tracks_details]
        tracks = await spotify_client.search.run(search_items)

        return [track[URI] for track in tracks][:MAX_SPOTIFY_PLAYLIST_SIZE]

    @staticmethod
    def _extract_user_text(request_body: dict) -> str:
        return request_body[PLAYLIST_DETAILS][PROMPT]
