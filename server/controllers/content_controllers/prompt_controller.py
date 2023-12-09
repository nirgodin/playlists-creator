from typing import List, Optional, Union, Type

from server.consts.api_consts import MAX_SPOTIFY_PLAYLIST_SIZE
from server.consts.app_consts import PLAYLIST_DETAILS, PROMPT
from server.consts.data_consts import URI
from server.consts.prompt_consts import QUERY_CONDITIONS_PROMPT_PREFIX_FORMAT, QUERY_CONDITIONS_PROMPT_SUFFIX_FORMAT, \
    TRACKS_AND_ARTISTS_NAMES_PROMPT_FORMAT
from server.consts.typing_consts import DataClass
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.playlist_resources import PlaylistResources
from server.data.prompt_details import PromptDetails
from server.logic.access_token_generator import AccessTokenGenerator
from server.logic.data_filterer import DataFilterer
from server.logic.openai.columns_details_creator import ColumnsDetailsCreator
from server.logic.openai.openai_adapter import OpenAIAdapter
from server.logic.openai.openai_client import OpenAIClient
from server.logic.openai.track_details import TrackDetails
from server.logic.playlist_cover_photo_creator import PlaylistCoverPhotoCreator
from server.logic.playlists_creator import PlaylistsCreator
from server.logic.prompt_details_tracks_selector import PromptDetailsTracksSelector
from server.logic.spotify_tracks_collector import SpotifyTracksCollector
from genie_common.tools.logs import logger
from server.utils.general_utils import build_prompt, to_dataclass
from server.utils.image_utils import current_timestamp_image_path


class PromptController(BaseContentController):
    def __init__(self,
                 playlists_creator: PlaylistsCreator,
                 playlists_cover_photo_creator: PlaylistCoverPhotoCreator,
                 openai_client: OpenAIClient,
                 access_token_generator: AccessTokenGenerator,
                 tracks_collector: SpotifyTracksCollector,
                 prompt_details_tracks_selector: PromptDetailsTracksSelector):
        super().__init__(playlists_creator, playlists_cover_photo_creator, openai_client, access_token_generator)
        self._openai_adapter = OpenAIAdapter(self._openai_client)
        self._tracks_collector = tracks_collector
        self._data_filterer = DataFilterer()
        self._columns_details_creator = ColumnsDetailsCreator()
        self._prompt_details_tracks_selector = prompt_details_tracks_selector

    async def _generate_playlist_resources(self, request_body: dict, dir_path: str) -> PlaylistResources:
        user_text = self._extract_prompt_from_request_body(request_body)
        query_conditions_uris = await self._generate_uris_from_prompt_details(user_text)

        if query_conditions_uris is not None:
            tracks_uris = query_conditions_uris
        else:
            tracks_uris = await self._generate_uris_from_tracks_details(user_text)

        return PlaylistResources(
            uris=tracks_uris,
            cover_image_path=current_timestamp_image_path(dir_path)
        )

    async def _generate_playlist_cover(self, request_body: dict, image_path: str) -> Optional[str]:
        user_text = self._extract_prompt_from_request_body(request_body)
        playlist_cover_prompt = f'{user_text}, digital art'

        return await self._openai_client.create_image(playlist_cover_prompt, image_path)

    async def _generate_uris_from_prompt_details(self, user_text: str) -> Optional[List[str]]:
        prompt = self._build_query_conditions_prompt(user_text)
        json_serialized_response = await self._openai_adapter.chat_completions(prompt, retries_left=1)
        prompt_details = self._serialize_openai_response(json_serialized_response, dataclass=PromptDetails)

        if prompt_details is not None:
            return await self._prompt_details_tracks_selector.select_tracks(prompt_details)

    def _build_query_conditions_prompt(self, user_text: str) -> str:
        columns_details = self._columns_details_creator.create()
        prompt_prefix = QUERY_CONDITIONS_PROMPT_PREFIX_FORMAT.format(columns_details=columns_details)
        prompt_suffix = QUERY_CONDITIONS_PROMPT_SUFFIX_FORMAT.format(user_text=user_text)

        return build_prompt(prompt_prefix, prompt_suffix)

    @staticmethod
    def _serialize_openai_response(json_serialized_response: Optional[Union[List[dict], dict]],
                                   dataclass: Type[DataClass]) -> Optional[Union[DataClass, List[DataClass]]]:
        try:
            if json_serialized_response is not None:
                return to_dataclass(json_serialized_response, dataclass)

        except:
            logger.exception("Could not serialize OpenAI response to dataclass. Returning None instead")

    async def _generate_uris_from_tracks_details(self, user_text: str) -> Optional[List[str]]:
        prompt = TRACKS_AND_ARTISTS_NAMES_PROMPT_FORMAT.format(user_text=user_text)
        json_serialized_response = await self._openai_adapter.chat_completions(prompt, retries_left=2)
        tracks_details = self._serialize_openai_response(json_serialized_response, dataclass=TrackDetails)

        if tracks_details is None:
            return

        tracks = await self._tracks_collector.collect(tracks_details)
        return [track[URI] for track in tracks][:MAX_SPOTIFY_PLAYLIST_SIZE]

    def _build_uris_prompt(self, user_text: str) -> str:
        columns_details = self._columns_details_creator.create()
        prompt_prefix = QUERY_CONDITIONS_PROMPT_PREFIX_FORMAT.format(columns_details=columns_details)
        prompt_suffix = QUERY_CONDITIONS_PROMPT_SUFFIX_FORMAT.format(user_text=user_text)

        return build_prompt(prompt_prefix, prompt_suffix)

    @staticmethod
    def _extract_prompt_from_request_body(request_body: dict) -> str:
        return request_body[PLAYLIST_DETAILS][PROMPT]
