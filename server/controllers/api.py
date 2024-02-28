import json
from typing import Annotated, Dict

from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette.background import BackgroundTasks

from server.component_factory import get_authenticator, get_request_body_controller, get_configuration_controller, \
    get_prompt_controller, get_photo_controller, get_existing_playlist_controller, get_wrapped_controller, \
    get_for_you_controller, get_case_progress_controller, get_playlist_controller, get_method_controller_mapping
from server.consts.app_consts import PHOTO
from server.controllers.case_progress_controller import CaseProgressController
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.controllers.content_controllers.configuration_controller import ConfigurationController
from server.controllers.content_controllers.existing_playlist_controller import ExistingPlaylistController
from server.controllers.content_controllers.for_you_controller import ForYouController
from server.controllers.content_controllers.photo_controller import PhotoController
from server.controllers.content_controllers.prompt_controller import PromptController
from server.controllers.content_controllers.wrapped_controller import WrappedController
from server.controllers.playlist_controller import PlaylistController
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


@api_router.post('/playlist/{method}')
async def playlist(method: str,
                   request: dict,
                   background_tasks: BackgroundTasks,
                   credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                   authenticator: Annotated[Authenticator, Depends(get_authenticator)],
                   method_controller_mapping: Annotated[Dict[str, BaseContentController], Depends(get_method_controller_mapping)],
                   playlist_controller: Annotated[PlaylistController, Depends(get_playlist_controller)]):
    authenticator.authenticate(credentials)
    controller = method_controller_mapping[method]
    background_tasks.add_task(controller.post, request_body=request)

    return await playlist_controller.post()


@api_router.post('/configuration')
async def configuration(request: dict,
                        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                        config_controller: Annotated[ConfigurationController, Depends(get_configuration_controller)]):
    return await config_controller.post(request_body=request, credentials=credentials)


@api_router.post('/prompt')
async def prompt(request: dict,
                 credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                 prompt_controller: Annotated[PromptController, Depends(get_prompt_controller)]):
    return await prompt_controller.post(request_body=request, credentials=credentials)


@api_router.post('/photo')
async def photos(photo: Annotated[UploadFile, File()],
                 body: Annotated[str, Form()],
                 credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                 authenticator: Annotated[Authenticator, Depends(get_authenticator)],
                 photo_controller: Annotated[PhotoController, Depends(get_photo_controller)]):
    authenticator.authenticate(credentials)
    request = json.loads(body)
    request[PHOTO] = await photo.read()

    return await photo_controller.post(request_body=request, credentials=credentials)


@api_router.post('/existingPlaylist')
async def existing_playlist(request: dict,
                            credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                            existing_playlist_controller: Annotated[
                                ExistingPlaylistController, Depends(get_existing_playlist_controller)]):
    return await existing_playlist_controller.post(request_body=request, credentials=credentials)


@api_router.post('/wrapped')
async def wrapped(request: dict,
                  credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                  wrapped_controller: Annotated[WrappedController, Depends(get_wrapped_controller)]):
    return await wrapped_controller.post(request_body=request, credentials=credentials)


@api_router.post('/forYou')
async def for_you(request: dict,
                  credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                  for_you_controller: Annotated[ForYouController, Depends(get_for_you_controller)]):
    return await for_you_controller.post(request_body=request, credentials=credentials)


@api_router.get('/caseProgress/{case_id}')
async def case_progress(case_id: str,
                        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                        authenticator: Annotated[Authenticator, Depends(get_authenticator)],
                        case_progress_controller: Annotated[CaseProgressController, Depends(get_case_progress_controller)]):
    authenticator.authenticate(credentials)
    return await case_progress_controller.get(case_id)
