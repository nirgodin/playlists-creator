from dataclasses_json.stringcase import camelcase
from flask import Response, jsonify
from flask_restful import Resource

from server.consts.app_consts import FILTER_PARAMS, ACCESS_CODE, PLAYLIST_DETAILS, PLAYLIST_NAME, PLAYLIST_DESCRIPTION, \
    IS_PUBLIC, PROMPT, OPERATOR, VALUE, LESS_THAN_OPERATOR, GREATER_THAN_OPERATOR, REQUEST_BODY, INCLUDE_NAN
from server.consts.openai_consts import IN_OPERATOR
from server.logic.openai.column_details import ColumnDetails
from server.logic.openai.columns_details_creator import ColumnsDetailsCreator
from server.utils.data_utils import load_data


class RequestBodyController(Resource):
    def __init__(self):
        self._columns_details_creator = ColumnsDetailsCreator()

    def get(self) -> Response:
        body = {
            FILTER_PARAMS: self._get_filter_params_defaults(),
            ACCESS_CODE: '',
            PLAYLIST_DETAILS: {
                PLAYLIST_NAME: '',
                PLAYLIST_DESCRIPTION: '',
                IS_PUBLIC: False,
                PROMPT: ''
            }
        }
        response = {
            REQUEST_BODY: [body]
        }

        return jsonify(response)

    def _get_filter_params_defaults(self) -> dict:
        data = load_data()
        filter_params = {}

        for column_details in self._columns_details_creator.get_relevant_columns_details(data):
            column_params = self._get_single_column_filter_params(column_details)
            filter_params.update(column_params)

        return filter_params

    def _get_single_column_filter_params(self, column_details: ColumnDetails) -> dict:
        if column_details.operator == IN_OPERATOR:
            return self._get_list_filter_param(column_details.name)

        else:
            return self._get_range_filter_param(column_details)

    @staticmethod
    def _get_list_filter_param(column_name: str) -> dict:
        return {
            camelcase(column_name): {
                OPERATOR: IN_OPERATOR,
                VALUE: [],
                INCLUDE_NAN: True
            }
        }

    @staticmethod
    def _get_range_filter_param(column_details: ColumnDetails) -> dict:
        return {
            camelcase(f'min_{column_details.name}'): {
                OPERATOR: GREATER_THAN_OPERATOR,
                VALUE: column_details.values[0]
            },
            camelcase(f'max_{column_details.name}'): {
                OPERATOR: LESS_THAN_OPERATOR,
                VALUE: column_details.values[1]
            }
        }
