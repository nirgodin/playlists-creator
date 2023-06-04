from flask import Response, jsonify
from flask_restful import Resource

from server.utils.general_utils import get_column_min_max_values


class MinMaxValuesController(Resource):
    def get(self, column_name: str) -> Response:
        res = {
            'minMaxValues': get_column_min_max_values(column_name)
        }
        response = jsonify(res)

        return response
