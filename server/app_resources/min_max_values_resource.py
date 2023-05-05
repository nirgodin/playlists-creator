from functools import lru_cache
from typing import List

from flask import Response, jsonify
from flask_restful import Resource

from server.utils import load_data, format_column_name


class MinMaxValues(Resource):
    def get(self, column_name: str) -> Response:
        res = {
            'minMaxValues': self._get_column_min_max_values(column_name)
        }
        response = jsonify(res)

        return response

    @staticmethod
    @lru_cache
    def _get_column_min_max_values(column_name: str) -> List[float]:
        data = load_data()
        formatted_column_name = format_column_name(column_name)
        min_value = float(data[formatted_column_name].min())
        max_value = float(data[formatted_column_name].max())

        return [min_value, max_value]
