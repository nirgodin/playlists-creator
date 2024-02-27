from http import HTTPStatus
from typing import Optional

from genie_datastores.postgres.models import CaseProgress
from genie_datastores.postgres.operations import execute_query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.responses import JSONResponse


class CaseProgressController:
    def __init__(self, db_engine: AsyncEngine):
        self._db_engine = db_engine

    async def get(self, case_id: str) -> JSONResponse:
        query = (
            select(CaseProgress.status)
            .where(CaseProgress.case_id == case_id)
            .order_by(CaseProgress.creation_date.desc())
            .limit(1)
        )
        query_result = await execute_query(engine=self._db_engine, query=query)
        status: Optional[str] = query_result.scalars().first()

        if status is None:
            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST.value,
                content={"message": "Did not find any record that matches the provided case id"}
            )

        return JSONResponse(
            status_code=HTTPStatus.OK.value,
            content={"caseStatus": status}
        )
