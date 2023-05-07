from flask import Response, jsonify
from flask_restful import Resource

from server.utils import get_column_possible_values


class PossibleValuesController(Resource):
    def get(self, column_name: str) -> Response:
        res = {
            'possibleValues': get_column_possible_values(column_name)
        }
        response = jsonify(res)

        return response
