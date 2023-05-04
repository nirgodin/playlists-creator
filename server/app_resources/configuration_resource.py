from flask import Response, request
from flask_restful import Resource

from server.logic.parameters_transformer import ParametersTransformer
from server.utils import generate_response


class Configuration(Resource):
    def post(self) -> Response:
        body = request.get_json()
        query_conditions = ParametersTransformer().transform(body)

        return generate_response(body, query_conditions)
