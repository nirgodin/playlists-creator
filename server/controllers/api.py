import json
from http import HTTPStatus
from typing import Annotated, Dict

from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from genie_datastores.postgres.models import PlaylistEndpoint
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse

from server.component_factory import get_authenticator, get_request_body_controller, get_photo_controller, \
    get_cases_controller, get_cases_manager, get_endpoint_controller_mapping
from server.consts.app_consts import PHOTO
from server.controllers.case_controller import CasesController
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.controllers.content_controllers.photo_controller import PhotoController
from server.logic.cases_manager import CasesManager
from server.controllers.request_body_controller import RequestBodyController
from server.tools.authenticator import Authenticator

api_router = APIRouter(prefix='/api')
security = HTTPBasic()


@api_router.get('/requestBody')
async def request_body(credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                       authenticator: Annotated[Authenticator, Depends(get_authenticator)],
                       request_body_controller: Annotated[RequestBodyController, Depends(get_request_body_controller)]):
    authenticator.authenticate(credentials)
    return await request_body_controller.get()


@api_router.post('/playlist/{endpoint}')
async def playlist(endpoint: PlaylistEndpoint,
                   request: dict,
                   background_tasks: BackgroundTasks,
                   credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                   authenticator: Annotated[Authenticator, Depends(get_authenticator)],
                   endpoint_controller_mapping: Annotated[Dict[PlaylistEndpoint, BaseContentController], Depends(get_endpoint_controller_mapping)],
                   cases_manager: Annotated[CasesManager, Depends(get_cases_manager)]):
    authenticator.authenticate(credentials)
    controller = endpoint_controller_mapping[endpoint]
    case_id = await cases_manager.create(endpoint)
    background_tasks.add_task(controller.post, request_body=request, case_id=case_id)  # TODO: pass case_id to content controller

    return JSONResponse(
        status_code=HTTPStatus.CREATED.value,
        content={"caseId": case_id}
    )


@api_router.post('/photo')
async def photos(photo: Annotated[UploadFile, File()],
                 body: Annotated[str, Form()],  # TODO: What to do with body not matching interface?
                 credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                 authenticator: Annotated[Authenticator, Depends(get_authenticator)],
                 photo_controller: Annotated[PhotoController, Depends(get_photo_controller)]):
    authenticator.authenticate(credentials)
    request = json.loads(body)
    request[PHOTO] = await photo.read()

    return await photo_controller.post(request_body=request, credentials=credentials)


@api_router.get('/cases/{case_id}/progress')
async def case_progress(case_id: str,
                        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                        authenticator: Annotated[Authenticator, Depends(get_authenticator)],
                        cases_controller: Annotated[CasesController, Depends(get_cases_controller)]):
    authenticator.authenticate(credentials)
    return await cases_controller.get_status(case_id)


@api_router.get('/cases/{case_id}/playlist')
async def case_playlist(case_id: str,
                        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                        authenticator: Annotated[Authenticator, Depends(get_authenticator)],
                        cases_controller: Annotated[CasesController, Depends(get_cases_controller)]):
    authenticator.authenticate(credentials)
    return await cases_controller.get_playlist_id(case_id)
