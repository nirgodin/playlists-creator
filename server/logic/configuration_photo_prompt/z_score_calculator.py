from typing import List

from cache import AsyncTTL
from genie_datastores.postgres.models import BaseORMModel
from genie_datastores.postgres.operations import execute_query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncEngine

from server.consts.general_consts import ONE_DAY_IN_SECONDS
from server.utils.statistics_utils import calculate_z_score


class ZScoreCalculator:
    def __init__(self, db_engine: AsyncEngine):
        self._db_engine = db_engine

    async def calculate(self, value: float, column: BaseORMModel):
        mean, std = await self._get_column_std_and_mean(column)
        return calculate_z_score(value, mean, std)

    @AsyncTTL(time_to_live=ONE_DAY_IN_SECONDS)
    async def _get_column_std_and_mean(self, column: BaseORMModel) -> List[float]:
        query = select(
            func.avg(column),
            func.stddev(column)
        )
        query_result = await execute_query(engine=self._db_engine, query=query)

        return [float(value) for value in query_result.first()]
