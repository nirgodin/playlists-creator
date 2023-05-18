import asyncio
from typing import List, Optional, TypeVar

from flask import Response, request

from server.consts.app_consts import PLAYLIST_DETAILS, PROMPT
from server.consts.openai_consts import QUERY_CONDITIONS_PROMPT_PREFIX_FORMAT, QUERY_CONDITIONS_PROMPT_SUFFIX_FORMAT, \
    TRACKS_AND_ARTISTS_NAMES_PROMPT_FORMAT
from server.controllers.base_content_controller import BaseContentController
from server.data.query_condition import QueryCondition
from server.logic.openai.columns_details_creator import ColumnsDetailsCreator
from server.logic.openai.openai_adapter import OpenAIAdapter
from server.logic.openai.track_details import TrackDetails
from server.logic.spotify_tracks_collector import SpotifyTracksCollector
from server.utils import build_prompt

DataClass = TypeVar('DataClass')


class PromptController(BaseContentController):
    def __init__(self):
        super().__init__()
        self._openai_adapter = OpenAIAdapter()
        self._columns_details_creator = ColumnsDetailsCreator()
        self._tracks_collector = SpotifyTracksCollector()

    def post(self) -> Response:
        body = request.get_json()
        user_text = body[PLAYLIST_DETAILS][PROMPT]
        # query_conditions = self._generate_query_conditions(user_text)
        #
        # if query_conditions is not None:
        #     return self._generate_response(body, query_conditions)
        # else:
        uris = self._generate_uris_from_prompt(user_text)
        return self._generate_response(body, [], uris)

    def _generate_query_conditions(self, user_text: str) -> Optional[List[QueryCondition]]:
        prompt = self._build_query_conditions_prompt(user_text)
        json_serialized_response = self._openai_adapter.fetch_openai(prompt, retries_left=1)

        return self._serialize_openai_response(json_serialized_response, klazz=QueryCondition)

    def _build_query_conditions_prompt(self, user_text: str) -> str:
        columns_details = self._columns_details_creator.create()
        prompt_prefix = QUERY_CONDITIONS_PROMPT_PREFIX_FORMAT.format(columns_details=columns_details)
        prompt_suffix = QUERY_CONDITIONS_PROMPT_SUFFIX_FORMAT.format(user_text=user_text)

        return build_prompt(prompt_prefix, prompt_suffix)

    @staticmethod
    def _serialize_openai_response(json_serialized_response: Optional[List[dict]], klazz: DataClass) -> Optional[list]:
        if json_serialized_response is None:
            return

        try:
            return [klazz.from_dict(condition) for condition in json_serialized_response]
        except:
            return

    def _generate_uris_from_prompt(self, user_text: str) -> Optional[List[str]]:
        prompt = TRACKS_AND_ARTISTS_NAMES_PROMPT_FORMAT.format(user_text)
        json_serialized_response = self._openai_adapter.fetch_openai(prompt, retries_left=1)
        tracks_details = self._serialize_openai_response(json_serialized_response, klazz=TrackDetails)

        if tracks_details is None:
            return

        return asyncio.run(self._tracks_collector.collect(tracks_details))

    def _build_uris_prompt(self, user_text: str) -> str:
        columns_details = self._columns_details_creator.create()
        prompt_prefix = QUERY_CONDITIONS_PROMPT_PREFIX_FORMAT.format(columns_details=columns_details)
        prompt_suffix = QUERY_CONDITIONS_PROMPT_SUFFIX_FORMAT.format(user_text=user_text)

        return build_prompt(prompt_prefix, prompt_suffix)
