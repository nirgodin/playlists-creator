from enum import Enum


class ZScoreDescription(Enum):
    LOW = (float('-inf'), -2)
    LOW_MEDIUM = (-2, -1)
    MEDIUM = (-1, 1)
    MEDIUM_HIGH = (1, 2)
    HIGH = (2, float('inf'))

    @staticmethod
    def get_z_score_description(z_score: float) -> str:
        for enum in ZScoreDescription:
            if enum.value[0] <= z_score < enum.value[1]:
                description: str = enum.name

                return description.replace('_', ' ').lower()
