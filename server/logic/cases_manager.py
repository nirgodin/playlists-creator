from genie_common.utils import random_alphanumeric_string
from genie_datastores.postgres.models import Case, PlaylistEndpoint, CaseProgress
from genie_datastores.postgres.operations import insert_records, execute_query
from genie_datastores.postgres.utils import update_by_values
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine

from server.data.case_status import CaseStatus
from server.tools.case_progress_reporter import CaseProgressReporter


class CasesManager:
    def __init__(self, db_engine: AsyncEngine, case_progress_reporter: CaseProgressReporter):
        self._db_engine = db_engine
        self._case_progress_reporter = case_progress_reporter

    async def create(self, endpoint: PlaylistEndpoint) -> str:
        case_id = random_alphanumeric_string(length=32)

        async with self._case_progress_reporter.report(case_id=case_id, status=CaseStatus.CREATED):
            case = Case(id=case_id, endpoint=endpoint)
            await insert_records(engine=self._db_engine, records=[case])

            return case_id

    async def get_case(self, case_id: str) -> Case:
        query = (
            select(Case)
            .where(Case.id == case_id)
            .limit(1)
        )
        query_result = await execute_query(engine=self._db_engine, query=query)

        return query_result.scalars().first()

    async def get_case_progress(self, case_id: str) -> CaseProgress:
        query = (
            select(CaseProgress)
            .where(CaseProgress.case_id == case_id)
            .order_by(CaseProgress.creation_date.desc())
            .limit(1)
        )
        query_result = await execute_query(engine=self._db_engine, query=query)

        return query_result.scalars().first()

    async def mark_completed(self, case_id: str, playlist_id: str) -> None:
        async with self._case_progress_reporter.report(case_id=case_id, status=CaseStatus.COMPLETED):
            await update_by_values(
                self._db_engine,
                Case,
                {Case.playlist_id: playlist_id},
                Case.id == case_id
            )
