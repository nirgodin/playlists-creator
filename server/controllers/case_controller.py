from http import HTTPStatus

from starlette.responses import JSONResponse

from server.consts.app_consts import MESSAGE
from server.consts.cases_consts import CASE_STATUS, PLAYLIST_ID, CASE_FAILURE_MESSAGE_FORMAT
from server.logic.cases_manager import CasesManager


class CasesController:
    def __init__(self, cases_manager: CasesManager):
        self._cases_manager = cases_manager

    async def get_status(self, case_id: str) -> JSONResponse:
        case_progress = await self._cases_manager.get_case_progress(case_id)

        if case_progress is None:
            return self._build_non_existing_case_response(case_id)

        return JSONResponse(
            status_code=HTTPStatus.OK.value,
            content={CASE_STATUS: case_progress.status}
        )

    async def get_playlist_id(self, case_id: str) -> JSONResponse:
        case = await self._cases_manager.get_case(case_id)

        if case is None:
            return self._build_non_existing_case_response(case_id)

        return JSONResponse(
            status_code=HTTPStatus.OK.value,
            content={PLAYLIST_ID: case.playlist_id}
        )

    @staticmethod
    def _build_non_existing_case_response(case_id: str) -> JSONResponse:
        message = CASE_FAILURE_MESSAGE_FORMAT.format(case_id=case_id)
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST.value,
            content={MESSAGE: message}
        )
