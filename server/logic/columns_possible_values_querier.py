from enum import EnumMeta
from typing import List

from genie_common.tools import AioPoolExecutor
from genie_datastores.postgres.models import BaseORMModel
from genie_datastores.postgres.operations import execute_query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncEngine

from server.data.column_group import ColumnGroup
from server.data.column_details import ColumnDetails


class ColumnsPossibleValuesQuerier:
    def __init__(self,
                 db_engine: AsyncEngine,
                 columns: List[BaseORMModel],
                 pool_executor: AioPoolExecutor = AioPoolExecutor()):
        self._db_engine = db_engine
        self._columns = columns
        self._pool_executor = pool_executor

    # TODO: Add here cache with TTL
    async def query(self) -> List[ColumnDetails]:
        return await self._pool_executor.run(
            iterable=self._columns,
            func=self._get_single_column_possible_values,
            expected_type=ColumnDetails
        )

    async def _get_single_column_possible_values(self, column: BaseORMModel) -> ColumnDetails:
        group = ColumnGroup.POSSIBLE_VALUES

        if column.type.python_type == bool:
            possible_values = [False, True]

        elif isinstance(column.type.python_type, EnumMeta):
            possible_values = column.type.enums

        elif column.type.python_type == str:
            possible_values = await self._query_possible_values(column)

        elif column.type.python_type in (int, float):
            possible_values = await self._query_min_max_values(column)
            group = ColumnGroup.MIN_MAX_VALUES

        else:
            raise ValueError(f"Column `{column.key}` has unknown type. Can't extract possible values")

        return ColumnDetails(
            name=column.key,
            values=sorted(possible_values),
            group=group
        )

    async def _query_possible_values(self, column: BaseORMModel) -> List[str]:
        query = (
            select(column)
            .distinct()
            .order_by(column.desc())
            .where(column.isnot(None))
        )
        query_result = await execute_query(engine=self._db_engine, query=query)

        return query_result.scalars().all()

    async def _query_min_max_values(self, column: BaseORMModel) -> List[float]:
        # TODO: Check if need to ceil and floor these values
        query = select(
            func.min(column),
            func.max(column)
        )
        query_result = await execute_query(engine=self._db_engine, query=query)

        return list(query_result.first())
