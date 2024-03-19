from contextlib import asynccontextmanager
from time import time

from genie_common.tools import logger
from genie_datastores.postgres.models import CaseProgress
from genie_datastores.postgres.operations import insert_records
from sqlalchemy.ext.asyncio import AsyncEngine

from server.data.case_status import CaseStatus


class CaseProgressReporter:
    def __init__(self, db_engine: AsyncEngine):
        self._db_engine = db_engine

    @asynccontextmanager
    async def report(self, case_id: str, status: CaseStatus) -> None:
        start_time = time()
        has_exception = False
        exception_details = None

        try:
            yield

        except Exception as e:
            logger.exception(f"Received exception! Marking status `{status.value}` with has_exception=True")
            has_exception = True
            exception_details = str(e)
            raise

        finally:
            record = CaseProgress(
                case_id=case_id,
                exception_details=exception_details,
                has_exception=has_exception,
                status=status.value,
                time_took=time() - start_time
            )
            await insert_records(engine=self._db_engine, records=[record])
