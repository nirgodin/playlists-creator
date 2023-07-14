from math import floor, ceil
from typing import List, Dict

from flask import Response, jsonify
from flask_restful import Resource

from server.consts.app_consts import FILTER_PARAMS, ACCESS_CODE, PLAYLIST_DETAILS, PLAYLIST_NAME, PLAYLIST_DESCRIPTION, \
    IS_PUBLIC, PROMPT, REQUEST_BODY, FEATURES_NAMES, FEATURES_VALUES, MIN_MAX_VALUES, POSSIBLE_VALUES, \
    FEATURES_DESCRIPTIONS, EXISTING_PLAYLIST
from server.logic.default_filter_params_generator import DefaultFilterParamsGenerator
from server.logic.features_descriptions_manager import FeaturesDescriptionsManager
from server.logic.features_names_generator import FeaturesNamesGenerator
from server.utils.general_utils import get_column_min_max_values, get_column_possible_values, format_column_name


class RequestBodyController(Resource):
    def __init__(self):
        self._default_filter_params_generator = DefaultFilterParamsGenerator()
        self._features_names_generator = FeaturesNamesGenerator()
        self._features_descriptions_manager = FeaturesDescriptionsManager()

    def get(self) -> Response:
        features_names = self._features_names_generator.generate_features_names()
        body = {
            FILTER_PARAMS: self._default_filter_params_generator.get_filter_params_defaults(),
            ACCESS_CODE: '',
            PLAYLIST_DETAILS: self._generate_default_playlist_details(),
            FEATURES_NAMES: self._features_names_generator.generate_features_names(),
            FEATURES_VALUES: self._get_features_values(features_names),
            FEATURES_DESCRIPTIONS: self._features_descriptions_manager.get_features_descriptions(),
        }
        response = {
            REQUEST_BODY: [body]
        }

        return jsonify(response)

    @staticmethod
    def _generate_default_playlist_details() -> dict:
        return {
            PLAYLIST_NAME: '',
            PLAYLIST_DESCRIPTION: '',
            IS_PUBLIC: False,
            PROMPT: '',
            EXISTING_PLAYLIST: ''
        }

    def _get_features_values(self, features_names: Dict[str, List[str]]) -> Dict[str, Dict[str, List[float]]]:
        min_max_values = self._get_min_max_features_values(features_names[MIN_MAX_VALUES])
        possible_values = {
            feature: get_column_possible_values(feature) for feature in features_names[POSSIBLE_VALUES]
        }

        return {
            MIN_MAX_VALUES: min_max_values,
            POSSIBLE_VALUES: possible_values
        }

    @staticmethod
    def _get_min_max_features_values(min_max_features: List[str]):
        min_max_values = {}

        for feature in min_max_features:
            formatted_feature_name = format_column_name(feature)
            min_value, max_value = get_column_min_max_values(formatted_feature_name)
            min_max_values[feature] = [ceil(min_value), floor(max_value)]

        return min_max_values
