from http import HTTPStatus
from typing import List, Dict, Any

from starlette.responses import JSONResponse

from server.consts.app_consts import REQUEST_BODY
from server.data.column_details import ColumnDetails
from server.data.column_group import ColumnGroup
from server.data.request_body.playlist_creation_request_body import PlaylistCreationRequestBody
from server.data.request_body.playlist_settings import PlaylistSettings
from server.logic.columns_possible_values_querier import ColumnsPossibleValuesQuerier
from server.logic.default_filter_params_generator import DefaultFilterParamsGenerator


class RequestBodyController:
    def __init__(self,
                 possible_values_querier: ColumnsPossibleValuesQuerier,
                 default_filter_params_generator: DefaultFilterParamsGenerator = DefaultFilterParamsGenerator()):
        self._possible_values_querier = possible_values_querier
        self._default_filter_params_generator = default_filter_params_generator

    async def get(self) -> JSONResponse:
        columns_values = await self._possible_values_querier.query()
        features_values = self._get_features_values(columns_values)
        body = PlaylistCreationRequestBody(
            filter_params=self._default_filter_params_generator.get_filter_params_defaults(columns_values),
            playlist_details=PlaylistSettings(),
            features_names=self._get_features_names(features_values),
            features_values=features_values,
            features_descriptions={column.formatted_name: column.description for column in columns_values},
        )
        content = {
            REQUEST_BODY: [body.to_dict()]
        }

        return JSONResponse(content=content, status_code=HTTPStatus.OK.value)

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
