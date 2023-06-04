from typing import Union, Dict, List, Optional

from server.consts.app_consts import VALUE
from server.logic.default_filter_params_generator import DefaultFilterParamsGenerator
from server.logic.z_score_calculator import ZScoreCalculator
from server.utils.string_utils import pre_process_column_name


class ConfigurationPhotoPromptCreator:
    def __init__(self):
        self._params_default_values = DefaultFilterParamsGenerator().get_filter_params_defaults()
        self._z_score_calculator = ZScoreCalculator()

    def create_prompt(self, filter_params: dict) -> Optional[str]:
        relevant_params = self._get_relevant_params_values(filter_params)

        if not relevant_params:
            return

        params_components = self._build_prompt_components(relevant_params)
        params_components.append(', digital art')

        return ' '.join(params_components)

    def _get_relevant_params_values(self, filter_params: dict) -> Dict[str, Union[float, list]]:
        relevant_params = {}

        for param_name, param_config in filter_params.items():
            param_value = param_config[VALUE]

            if not self._is_default_value(param_name, param_value):
                relevant_params[param_name] = param_value

        return relevant_params

    def _is_default_value(self, param_name: str, param_value: Union[float, list]) -> bool:
        if isinstance(param_value, list):
            return False if param_value else True

        return param_value == self._params_default_values[param_name][VALUE]

    def _build_prompt_components(self, relevant_params: Dict[str, Union[float, list]]) -> List[str]:
        prompt_components = []

        for param_name, param_value in relevant_params.items():
            param_prompt_component = self._build_single_param_prompt_line(param_name, param_value)
            prompt_components.append(param_prompt_component)

        return prompt_components

    def _build_single_param_prompt_line(self, param_name: str, param_value: Union[float, list]) -> str:
        formatted_param_name = pre_process_column_name(param_name)

        if isinstance(param_value, list):
            return self._build_list_param_prompt(formatted_param_name, param_value)
        else:
            return self._build_numeric_param_prompt(formatted_param_name, param_value)

    @staticmethod
    def _build_list_param_prompt(param_name: str, param_value: list) -> str:
        joined_values = ', '.join(param_value)
        return f'{param_name} is one of the following: {joined_values}'

    def _build_numeric_param_prompt(self, param_name: str, param_value: float) -> str:
        z_score = self._z_score_calculator.calculate(param_value, param_name)

        if z_score < -1:
            return f'non {param_name}'  # TODO: Consider max and min suffix and map to adjectives
        elif z_score > 1:
            return f'highly {param_name}'
        else:
            return f'average {param_name}'
