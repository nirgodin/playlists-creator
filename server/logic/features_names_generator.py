from typing import List, Dict

from server.consts.app_consts import MIN_MAX_VALUES, POSSIBLE_VALUES
from server.consts.openai_consts import NUMERIC_OPERATORS, IN_OPERATOR
from server.logic.openai.column_details import ColumnDetails
from server.logic.openai.columns_details_creator import ColumnsDetailsCreator
from server.utils.data_utils import load_data
from server.utils.general_utils import titleize_feature_name


class FeaturesNamesGenerator:
    def __init__(self):
        self._columns_details_creator = ColumnsDetailsCreator()
        self._data = load_data()

    def generate_features_names(self) -> Dict[str, List[str]]:
        columns_details = list(self._columns_details_creator.get_relevant_columns_details(self._data))
        return {
            MIN_MAX_VALUES: self._get_relevant_features_names(columns_details, NUMERIC_OPERATORS),
            POSSIBLE_VALUES: self._get_relevant_features_names(columns_details, IN_OPERATOR)
        }

    @staticmethod
    def _get_relevant_features_names(columns_details: List[ColumnDetails], operator: str) -> List[str]:
        features_names = []

        for column in columns_details:
            if column.operator == operator:
                formatted_feature_name = titleize_feature_name(column.name)
                features_names.append(formatted_feature_name)

        return sorted(features_names)
