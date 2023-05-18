from flask import Response, request

from server.controllers.base_content_controller import BaseContentController
from server.logic.parameters_transformer import ParametersTransformer


class ConfigurationController(BaseContentController):
    def __init__(self):
        super().__init__()

    def post(self) -> Response:
        body = request.get_json()
        query_conditions = ParametersTransformer().transform(body)
        uris = self._data_filterer.filter(query_conditions)

        return self._generate_response(body, uris)
