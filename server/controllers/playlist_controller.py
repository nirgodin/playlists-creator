from genie_common.utils import random_alphanumeric_string
from genie_datastores.postgres.models import Case, PlaylistEndpoint
from genie_datastores.postgres.operations import insert_records
from sqlalchemy.ext.asyncio import AsyncEngine

from server.tools.case_progress_reporter import CaseProgressReporter


class PlaylistController:  # TODO: Rename to other name than `controller`
    def __init__(self, db_engine: AsyncEngine, case_progress_reporter: CaseProgressReporter):
        self._db_engine = db_engine
        self._case_progress_reporter = case_progress_reporter

    async def create(self, endpoint: PlaylistEndpoint) -> str:
        case_id = random_alphanumeric_string(length=32)

        async with self._case_progress_reporter.report(case_id=case_id, status="created"):
            case = Case(id=case_id, endpoint=endpoint)
            await insert_records(engine=self._db_engine, records=[case])

            return case_id
