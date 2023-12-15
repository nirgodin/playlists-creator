from typing import Union, Dict, List

from server.consts.app_consts import VALUE, GREATER_THAN_OPERATOR, LESS_THAN_OPERATOR
from server.consts.data_consts import IN_OPERATOR
from server.data.z_score_description import ZScoreDescription
from server.data.prompt_component import PromptComponent
from server.logic.configuration_photo_prompt.z_score_calculator import ZScoreCalculator
from server.utils.string_utils import pre_process_column_name


class ConfigurationPhotoPromptCreator:
    def __init__(self, params_default_values: dict, z_score_calculator: ZScoreCalculator):
        self._params_default_values = params_default_values
        self._z_score_calculator = z_score_calculator

    async def create_prompt(self, filter_params: dict) -> str:
        relevant_params = self._get_relevant_params_values(filter_params)

        if not relevant_params:
            return 'Cool music related image with high contrast and vivid colors, digital art'

        params_components = await self._build_prompt_components(relevant_params)
        params_components.append(', digital art')
        songs_description = '; '.join(params_components)

        return f'Songs with the following characteristics: {songs_description}'

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

    async def _build_prompt_components(self, relevant_params: Dict[str, Union[float, list]]) -> List[str]:
        raw_prompt_components = []

        for param_name, param_value in relevant_params.items():
            param_prompt_component = await self._build_single_param_prompt_line(param_name, param_value)
            raw_prompt_components.append(param_prompt_component)

        return self._process_raw_prompt_components(raw_prompt_components)

    async def _build_single_param_prompt_line(self, param_name: str, param_value: Union[float, list]) -> PromptComponent:
        formatted_param_name = pre_process_column_name(param_name)

        if isinstance(param_value, list):
            return self._build_list_param_prompt(formatted_param_name, param_value)
        else:
            return await self._build_numeric_param_prompt(param_name, formatted_param_name, param_value)

    @staticmethod
    def _build_list_param_prompt(param_name: str, param_value: list) -> PromptComponent:
        return PromptComponent(
            name=param_name.replace('_', ' '),
            description=', '.join(param_value),
            param_type=IN_OPERATOR
        )

    async def _build_numeric_param_prompt(self, raw_param_name: str, formatted_param_name: str, param_value: float) -> PromptComponent:
        z_score = await self._z_score_calculator.calculate(param_value, formatted_param_name)
        description = ZScoreDescription.get_z_score_description(z_score)
        param_type = GREATER_THAN_OPERATOR if raw_param_name.startswith('min') else LESS_THAN_OPERATOR

        return PromptComponent(
            name=formatted_param_name,
            description=description,
            param_type=param_type
        )

    def _process_raw_prompt_components(self, raw_prompt_components: List[PromptComponent]) -> List[str]:
        unique_components_names = {component.name for component in raw_prompt_components}
        processed_components = []

        for component_name in unique_components_names:
            relevant_components = [component for component in raw_prompt_components if component.name == component_name]

            if len(relevant_components) == 1:
                processed_component = self._process_single_component_prompt(relevant_components[0])
            else:
                processed_component = self._process_multi_component_prompt(relevant_components)

            processed_components.append(processed_component)

        return processed_components

    @staticmethod
    def _process_single_component_prompt(component: PromptComponent) -> str:
        if component.param_type == IN_OPERATOR:
            return f'{component.name} is one of the following: {component.description}'

        elif component.param_type == GREATER_THAN_OPERATOR:
            return f'{component.name} is from {component.description} to high'

        elif component.param_type == LESS_THAN_OPERATOR:
            return f'{component.name} is from low to {component.description}'

        else:
            raise ValueError(f'Unsupported param type: `{component.param_type}`')

    def _process_multi_component_prompt(self, components: List[PromptComponent]) -> str:
        component_name = components[0].name
        min_component_index = self._get_minimum_component_index(components)
        min_component_description = components[min_component_index].description
        max_component_description = components[min_component_index - 1].description

        if min_component_description == max_component_description:
            return f'{component_name} is {min_component_description}'

        return f'{component_name} is from {min_component_description} to {max_component_description}'

    @staticmethod
    def _get_minimum_component_index(components: List[PromptComponent]) -> int:
        for i, component in enumerate(components):
            if component.param_type == GREATER_THAN_OPERATOR:
                return i
