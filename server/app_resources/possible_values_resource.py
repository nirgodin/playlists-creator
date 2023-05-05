from functools import lru_cache
from typing import List

import pandas as pd
from flask import Response, jsonify
from flask_restful import Resource

from server.utils import load_data, format_column_name


class PossibleValues(Resource):
    def get(self, column_name: str) -> Response:
        res = {
            'possibleValues': self._get_column_possible_values(column_name)
        }
        response = jsonify(res)

        return response

    @staticmethod
    @lru_cache
    def _get_column_possible_values(column_name: str) -> List[float]:
        data = load_data()
        formatted_column_name = format_column_name(column_name)
        unique_values = data[formatted_column_name].unique().tolist()

        return sorted([value for value in unique_values if not pd.isna(value)])
