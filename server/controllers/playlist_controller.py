import time
from http import HTTPStatus

from genie_common.utils import random_alphanumeric_string
from genie_datastores.postgres.models import Case, CaseProgress
from genie_datastores.postgres.operations import insert_records
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.responses import JSONResponse


class PlaylistController:
    def __init__(self, db_engine: AsyncEngine):
        self._db_engine = db_engine

    async def post(self) -> JSONResponse:
        start_time = time.time()
        case_id = random_alphanumeric_string(length=32)
        case = Case(id=case_id)
        await insert_records(engine=self._db_engine, records=[case])
        case_progress = CaseProgress(
            case_id=case_id,
            status="created",
            time_took=time.time() - start_time
        )
        await insert_records(engine=self._db_engine, records=[case_progress])

        return JSONResponse(
            status_code=HTTPStatus.CREATED.value,
            content={"caseId": case_id}
        )
