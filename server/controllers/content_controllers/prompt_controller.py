from base64 import b64decode
from typing import List, Optional, Union, Type

from genie_common.models.openai import ImageSize, DallEModel
from genie_common.tools.logs import logger
from genie_common.typing import Json
from spotipyio import SpotifyClient

from server.consts.api_consts import MAX_SPOTIFY_PLAYLIST_SIZE
from server.consts.app_consts import PLAYLIST_DETAILS, PROMPT
from server.consts.data_consts import URI
from server.consts.prompt_consts import QUERY_CONDITIONS_PROMPT_PREFIX_FORMAT, QUERY_CONDITIONS_PROMPT_SUFFIX_FORMAT, \
    TRACKS_AND_ARTISTS_NAMES_PROMPT_FORMAT
from server.consts.typing_consts import DataClass
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.chat_completions_request import ChatCompletionsRequest
from server.data.playlist_creation_context import PlaylistCreationContext
from server.data.playlist_resources import PlaylistResources
from server.data.prompt_details import PromptDetails
from server.data.track_details import TrackDetails
from server.logic.openai.columns_descriptions_creator import ColumnsDescriptionsCreator
from server.logic.openai.openai_adapter import OpenAIAdapter
from server.logic.prompt_details_tracks_selector import PromptDetailsTracksSelector
from server.utils.general_utils import build_prompt, to_dataclass
from server.utils.image_utils import current_timestamp_image_path, save_image_from_bytes


class PromptController(BaseContentController):
    def __init__(self,
                 context: PlaylistCreationContext,
                 openai_adapter: OpenAIAdapter,
                 prompt_details_tracks_selector: PromptDetailsTracksSelector,
                 columns_descriptions_creator: ColumnsDescriptionsCreator):
        super().__init__(context)
        self._openai_adapter = openai_adapter
        self._columns_descriptions_creator = columns_descriptions_creator
        self._prompt_details_tracks_selector = prompt_details_tracks_selector

    async def _generate_playlist_resources(self,
                                           case_id: str,
                                           request_body: dict,
                                           dir_path: str,
                                           spotify_client: SpotifyClient) -> PlaylistResources:
        user_text = self._extract_prompt_from_request_body(request_body)
        query_conditions_uris = await self._generate_uris_from_prompt_details(case_id, user_text)

        if query_conditions_uris is not None:
            tracks_uris = query_conditions_uris
        else:
            tracks_uris = await self._generate_uris_from_tracks_details(case_id, user_text, spotify_client)

        return PlaylistResources(
            uris=tracks_uris,
            cover_image_path=current_timestamp_image_path(dir_path)
        )

    async def _generate_playlist_cover(self, request_body: dict, image_path: str) -> Optional[str]:
        user_text = self._extract_prompt_from_request_body(request_body)
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

    async def _generate_uris_from_prompt_details(self, case_id: str, user_text: str) -> Optional[List[str]]:
        prompt = await self._build_query_conditions_prompt(user_text)
        request = ChatCompletionsRequest(
            prompt=prompt,
            expected_type=dict
        )
        response: Optional[Json] = await self._openai_adapter.chat_completions(request)
        prompt_details: PromptDetails = self._serialize_openai_response(response, dataclass=PromptDetails)

        if prompt_details is not None:
            return await self._prompt_details_tracks_selector.select_tracks(case_id, prompt_details)

    async def _build_query_conditions_prompt(self, user_text: str) -> str:
        columns_details = await self._columns_descriptions_creator.create()
        prompt_prefix = QUERY_CONDITIONS_PROMPT_PREFIX_FORMAT.format(columns_details=columns_details)
        prompt_suffix = QUERY_CONDITIONS_PROMPT_SUFFIX_FORMAT.format(user_text=user_text)

        return build_prompt(prompt_prefix, prompt_suffix)

    @staticmethod
    def _serialize_openai_response(response: Optional[Json],
                                   dataclass: Type[DataClass]) -> Optional[Union[DataClass, List[DataClass]]]:
        try:
            if response is not None:
                return to_dataclass(response, dataclass)

        except:
            logger.exception("Could not serialize OpenAI response to dataclass. Returning None instead")

    async def _generate_uris_from_tracks_details(self,
                                                 case_id: str,
                                                 user_text: str,
                                                 spotify_client: SpotifyClient) -> Optional[List[str]]:
        prompt = TRACKS_AND_ARTISTS_NAMES_PROMPT_FORMAT.format(user_text=user_text)
        request = ChatCompletionsRequest(
            prompt=prompt,
            expected_type=list,
            retries_left=2
        )
        response = await self._openai_adapter.chat_completions(request)
        tracks_details: List[TrackDetails] = self._serialize_openai_response(response, dataclass=TrackDetails)

        if tracks_details is not None:  # TODO: Add case progress
            search_items = [details.to_search_item() for details in tracks_details]
            tracks = await spotify_client.search.run(search_items)

            return [track[URI] for track in tracks][:MAX_SPOTIFY_PLAYLIST_SIZE]

    @staticmethod
    def _extract_prompt_from_request_body(request_body: dict) -> str:
        return request_body[PLAYLIST_DETAILS][PROMPT]
