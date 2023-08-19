import json
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from server.component_factory import get_authenticator, get_request_body_controller, get_configuration_controller, \
    get_prompt_controller, get_photo_controller, get_existing_playlist_controller
from server.consts.app_consts import PHOTO
from server.controllers.content_controllers.configuration_controller import ConfigurationController
from server.controllers.content_controllers.existing_playlist_controller import ExistingPlaylistController
from server.controllers.content_controllers.photo_controller import PhotoController
from server.controllers.content_controllers.prompt_controller import PromptController
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


@api_router.post('/configuration')
async def configuration(request: dict,
                        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                        authenticator: Annotated[Authenticator, Depends(get_authenticator)],
                        config_controller: Annotated[ConfigurationController, Depends(get_configuration_controller)]):
    authenticator.authenticate(credentials)
    return await config_controller.post(request)


@api_router.post('/prompt')
async def prompt(request: dict,
                 credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                 authenticator: Annotated[Authenticator, Depends(get_authenticator)],
                 prompt_controller: Annotated[PromptController, Depends(get_prompt_controller)]):
    authenticator.authenticate(credentials)
    return await prompt_controller.post(request)


@api_router.post('/photo')
async def photos(photo: Annotated[UploadFile, File()],
                 body: Annotated[str, Form()],
                 credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                 authenticator: Annotated[Authenticator, Depends(get_authenticator)],
                 photo_controller: Annotated[PhotoController, Depends(get_photo_controller)]):
    authenticator.authenticate(credentials)
    request = json.loads(body)
    request[PHOTO] = await photo.read()

    return await photo_controller.post(request)


@api_router.post('/existingPlaylist')
async def existing_playlist(request: dict,
                            credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                            authenticator: Annotated[Authenticator, Depends(get_authenticator)],
                            existing_playlist_controller: Annotated[ExistingPlaylistController, Depends(get_existing_playlist_controller)]):
    authenticator.authenticate(credentials)
    return await existing_playlist_controller.post(request)