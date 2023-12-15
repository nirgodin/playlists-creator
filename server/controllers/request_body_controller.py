from typing import List, Dict, Any

from starlette.responses import JSONResponse

from server.consts.app_consts import FILTER_PARAMS, ACCESS_CODE, PLAYLIST_DETAILS, PLAYLIST_NAME, PLAYLIST_DESCRIPTION, \
    IS_PUBLIC, PROMPT, REQUEST_BODY, FEATURES_NAMES, FEATURES_VALUES, FEATURES_DESCRIPTIONS, EXISTING_PLAYLIST
from server.logic.default_filter_params_generator import DefaultFilterParamsGenerator
from server.logic.features_descriptions_manager import FeaturesDescriptionsManager
from server.logic.request_body.column_group import ColumnGroup
from server.logic.request_body.column_values import ColumnValues
from server.logic.request_body.columns_possible_values_querier import ColumnsPossibleValuesQuerier


class RequestBodyController:
    def __init__(self,
                 possible_values_querier: ColumnsPossibleValuesQuerier,
                 default_filter_params_generator: DefaultFilterParamsGenerator = DefaultFilterParamsGenerator(),
                 features_descriptions_manager: FeaturesDescriptionsManager = FeaturesDescriptionsManager()):
        self._possible_values_querier = possible_values_querier
        self._default_filter_params_generator = default_filter_params_generator
        self._features_descriptions_manager = features_descriptions_manager

    async def get(self) -> JSONResponse:
        columns_values = await self._possible_values_querier.query()
        features_values = self._get_features_values(columns_values)
        body = {
            FILTER_PARAMS: self._default_filter_params_generator.get_filter_params_defaults(),
            ACCESS_CODE: '',
            PLAYLIST_DETAILS: self._generate_default_playlist_details(),
            FEATURES_NAMES: self._get_features_names(features_values),
            FEATURES_VALUES: features_values,
            FEATURES_DESCRIPTIONS: self._features_descriptions_manager.get_features_descriptions(),
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
    def _get_features_values(columns_values: List[ColumnValues]) -> Dict[str, Dict[str, List[Any]]]:
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
