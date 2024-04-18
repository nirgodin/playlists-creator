from server.consts.prompt_consts import SINGLE_COLUMN_DESCRIPTION_FORMAT
from server.data.column_details import ColumnDetails
from server.logic.columns_possible_values_querier import ColumnsPossibleValuesQuerier


class ColumnsDescriptionsCreator:
    def __init__(self, possible_values_querier: ColumnsPossibleValuesQuerier):
        self._possible_values_querier = possible_values_querier

    async def create(self) -> str:
        columns_descriptions = []
        columns_details = await self._possible_values_querier.query()

        for i, column_details in enumerate(columns_details):
            column_description = self._build_single_column_description(i, column_details)
            columns_descriptions.append(column_description)

        return ''.join(columns_descriptions)

    @staticmethod
    def _build_single_column_description(index: int, column_details: ColumnDetails) -> str:
        return SINGLE_COLUMN_DESCRIPTION_FORMAT.format(
            column_index=index + 1,
            column_name=column_details.name,
            column_operator=column_details.operator,
            column_values=column_details.values,
            column_description=column_details.description
        )
