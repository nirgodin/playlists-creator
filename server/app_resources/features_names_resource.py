from typing import List

from flask import Response, jsonify
from flask_restful import Resource

from server.consts.app_consts import REQUEST_BODY, MIN_MAX_VALUES, FEATURES_NAMES
from server.consts.openai_consts import NUMERIC_OPERATORS, IN_OPERATOR
from server.logic.openai.column_details import ColumnDetails
from server.logic.openai.columns_details_creator import ColumnsDetailsCreator
from server.utils import load_data


class FeaturesNames(Resource):
    def __init__(self):
        self._columns_details_creator = ColumnsDetailsCreator()

    def get(self, feature_type: str) -> Response:
        features_names = self._get_features_names(feature_type)
        response = {
            FEATURES_NAMES: features_names
        }

        return jsonify(response)

    def _get_features_names(self, feature_type: str) -> List[str]:
        data = load_data()
        columns_details = list(self._columns_details_creator.get_relevant_columns_details(data))

        if feature_type == MIN_MAX_VALUES:
            return self._get_relevant_features_names(columns_details, NUMERIC_OPERATORS)

        else:
            return self._get_relevant_features_names(columns_details, IN_OPERATOR)

    def _get_relevant_features_names(self, columns_details: List[ColumnDetails], operator: str) -> List[str]:
        features_names = []

        for column in columns_details:
            if column.operator == operator:
                formatted_feature_name = self._format_feature_name(column.name)
                features_names.append(formatted_feature_name)

        return sorted(features_names)

    @staticmethod
    def _format_feature_name(column_name: str) -> str:
        column_tokens = column_name.split('_')
        formatted_tokens = [column_token.capitalize() for column_token in column_tokens]

        return ' '.join(formatted_tokens)
