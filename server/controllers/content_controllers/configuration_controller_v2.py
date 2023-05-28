from typing import List, Optional

from flask import Request

from server.controllers.content_controllers.base_content_controller_v2 import BaseContentControllerV2
from server.logic.data_filterer import DataFilterer
from server.logic.parameters_transformer import ParametersTransformer


class ConfigurationControllerV2(BaseContentControllerV2):
    def __init__(self):
        super(ConfigurationControllerV2).__init__()
        self._data_filterer = DataFilterer()
        self._parameters_transformer = ParametersTransformer()

    def _get_request_body(self, client_request: Request) -> dict:
        return client_request.get_json()

    def _generate_tracks_uris(self, request_body: dict) -> Optional[List[str]]:
        query_conditions = self._parameters_transformer.transform(request_body)
        return self._data_filterer.filter(query_conditions)

    def _generate_playlist_cover_prompt(self, request_body: dict) -> str:
        raise   # TODO: Fix to enable cover
