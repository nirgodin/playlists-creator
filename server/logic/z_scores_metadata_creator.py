import json
from typing import Dict

from pandas import DataFrame
from pandas.core.dtypes.common import is_numeric_dtype

from server.consts.data_consts import COLUMNS_Z_SCORES_METADATA_PATH
from server.data.column_z_score_metadata import ColumnZScoreMetadata
from server.utils import load_data


class ZScoresMetadataCreator:
    def create(self) -> None:
        data = load_data()
        columns_metadata = self._get_relevant_columns_metadata(data)

        with open(COLUMNS_Z_SCORES_METADATA_PATH, 'w') as f:
            json.dump(columns_metadata, f, indent=4)

    def _get_relevant_columns_metadata(self, data: DataFrame) -> Dict[str, Dict[str, float]]:
        columns_metadata = {}

        for column in data.columns:
            if not is_numeric_dtype(data[column]):
                continue

            column_metadata = self._calculate_single_column_metadata(data, column)
            columns_metadata[column] = column_metadata.to_dict()

        return columns_metadata

    @staticmethod
    def _calculate_single_column_metadata(data: DataFrame, column: str) -> ColumnZScoreMetadata:
        return ColumnZScoreMetadata(
            std=float(data[column].dropna().std()),
            mean=float(data[column].dropna().mean())
        )


if __name__ == '__main__':
    ZScoresMetadataCreator().create()
