from typing import Optional

from aiohttp import ClientSession
from flask import Request

from server.consts.app_consts import FILTER_PARAMS
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.playlist_resources import PlaylistResources
from server.logic.configuration_photo_prompt.configuration_photo_prompt_creator import ConfigurationPhotoPromptCreator
from server.logic.data_filterer import DataFilterer
from server.logic.parameters_transformer import ParametersTransformer
from server.utils.image_utils import current_timestamp_image_path


class ConfigurationController(BaseContentController):
    def __init__(self, session: ClientSession):
        super().__init__(session)
        self._data_filterer = DataFilterer()
        self._parameters_transformer = ParametersTransformer()
        self._photo_prompt_creator = ConfigurationPhotoPromptCreator()

    def _get_request_body(self, client_request: Request) -> dict:
        return client_request.get_json()

    async def _generate_playlist_resources(self, request_body: dict, dir_path: str) -> PlaylistResources:
        query_conditions = self._parameters_transformer.transform(request_body)
        tracks_uris = self._data_filterer.filter(query_conditions)

        return PlaylistResources(
            uris=tracks_uris,
            cover_image_path=current_timestamp_image_path(dir_path)
        )

    async def _generate_playlist_cover(self, request_body: dict, image_path: str) -> Optional[str]:
        raise
        filter_params = request_body[FILTER_PARAMS]
        playlist_cover_prompt = self._photo_prompt_creator.create_prompt(filter_params)

        return await self._openai_client.create_image(playlist_cover_prompt, image_path)
