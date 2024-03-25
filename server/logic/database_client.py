from typing import List, Dict, Set

from genie_common.tools import logger
from genie_datastores.postgres.models import RadioTrack, BaseORMModel
from genie_datastores.postgres.operations import execute_query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import Select
from sqlalchemy.sql.elements import BinaryExpression

from server.data.query_condition import QueryCondition


class DatabaseClient:
    def __init__(self,
                 db_engine: AsyncEngine,
                 columns: List[BaseORMModel],
                 orm_conditions_map: Dict[BaseORMModel, List[BinaryExpression]]):
        self._db_engine = db_engine
        self._columns = columns
        self._orm_conditions_map = orm_conditions_map

    async def query(self, query_conditions: List[QueryCondition]) -> List[str]:
        logger.info("Starting to query database for relevant tracks ids")
        query = self._build_query(query_conditions)
        query_result = await execute_query(engine=self._db_engine, query=query)
        tracks_ids = query_result.scalars().all()
        logger.info(f"Successfully queried database and found `{len(tracks_ids)}` relevant tracks")

        return tracks_ids

    def _build_query(self, query_conditions: List[QueryCondition]) -> Select:
        valid_conditions = [condition for condition in query_conditions if condition.value]
        orms = self._get_relevant_orms(valid_conditions)
        join_conditions = self._get_relevant_join_conditions(orms)
        filter_conditions = self._get_relevant_filter_conditions(valid_conditions)

        return (
            select(RadioTrack.track_id)
            .distinct(RadioTrack.track_id)
            .where(*join_conditions)
            .where(*filter_conditions)
        )

    def _get_relevant_orms(self, query_conditions: List[QueryCondition]) -> Set[BaseORMModel]:
        orms = set()

        for condition in query_conditions:
            orm = self._get_single_condition_orm(condition)
            orms.add(orm)

        return orms

    def _get_single_condition_orm(self, condition: QueryCondition) -> BaseORMModel:
        for column in self._columns:
            if column.key == condition.column:
                return column

        raise ValueError("Did not find query condition ORM")

    def _get_relevant_join_conditions(self, orms: Set[BaseORMModel]) -> List[BinaryExpression]:
        join_conditions = []

        for orm in orms:
            conditions = self._orm_conditions_map[orm.class_]

            for condition in conditions:
                if self._is_new_condition(condition, join_conditions):
                    join_conditions.append(condition)

        return join_conditions

    @staticmethod
    def _is_new_condition(new_condition: BinaryExpression, existing_conditions: List[BinaryExpression]) -> bool:
        return not any(condition.compare(new_condition) for condition in existing_conditions)

    def _get_relevant_filter_conditions(self, query_conditions: List[QueryCondition]) -> List[BinaryExpression]:
        filter_conditions = []

        for query_condition in query_conditions:
            orm = self._get_single_condition_orm(query_condition)
            method = self._operators_methods_mapping[query_condition.operator]
            condition = getattr(orm, method)(query_condition.value)
            filter_conditions.append(condition)

        return filter_conditions

    @property
    def _operators_methods_mapping(self) -> Dict[str, str]:
        return {
            "in": "in_",
            "<=": "__le__",
            ">=": "__ge__"
        }
