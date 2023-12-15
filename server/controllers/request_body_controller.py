from typing import List, Dict, Any

from starlette.responses import JSONResponse

from server.consts.app_consts import FILTER_PARAMS, ACCESS_CODE, PLAYLIST_DETAILS, PLAYLIST_NAME, PLAYLIST_DESCRIPTION, \
    IS_PUBLIC, PROMPT, REQUEST_BODY, FEATURES_NAMES, FEATURES_VALUES, FEATURES_DESCRIPTIONS, EXISTING_PLAYLIST
from server.logic.default_filter_params_generator import DefaultFilterParamsGenerator
from server.data.column_group import ColumnGroup
from server.data.column_details import ColumnDetails
from server.logic.columns_possible_values_querier import ColumnsPossibleValuesQuerier


class RequestBodyController:
    def __init__(self,
                 possible_values_querier: ColumnsPossibleValuesQuerier,
                 default_filter_params_generator: DefaultFilterParamsGenerator = DefaultFilterParamsGenerator()):
        self._possible_values_querier = possible_values_querier
        self._default_filter_params_generator = default_filter_params_generator

    async def get(self) -> JSONResponse:
        columns_values = await self._possible_values_querier.query()
        features_values = self._get_features_values(columns_values)
        body = {
            FILTER_PARAMS: self._default_filter_params_generator.get_filter_params_defaults(columns_values),
            ACCESS_CODE: '',
            PLAYLIST_DETAILS: self._generate_default_playlist_details(),
            FEATURES_NAMES: self._get_features_names(features_values),
            FEATURES_VALUES: features_values,
            FEATURES_DESCRIPTIONS: {column.formatted_name: column.description for column in columns_values},
        }
        content = {
            REQUEST_BODY: [body]
        }

        return JSONResponse(content=content, status_code=200)

    @staticmethod
    def _generate_default_playlist_details() -> dict:
        return {
            PLAYLIST_NAME: '',
            PLAYLIST_DESCRIPTION: '',
            IS_PUBLIC: False,
            PROMPT: '',
            EXISTING_PLAYLIST: ''
        }

    @staticmethod
    def _get_features_values(columns_values: List[ColumnDetails]) -> Dict[str, Dict[str, List[Any]]]:
        features_values = {
            ColumnGroup.MIN_MAX_VALUES.value: {},
            ColumnGroup.POSSIBLE_VALUES.value: {},
        }

        for column in columns_values:
            features_values[column.group.value][column.formatted_name] = column.values

        return features_values

    @staticmethod
    def _get_features_names(features_values: Dict[str, Dict[str, List[Any]]]) -> Dict[str, List[str]]:
        features_names = {}

        for group in features_values.keys():
            group_features = features_values[group]
            features_names[group] = list(group_features.keys())

        return features_names
