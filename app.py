import json
from typing import Annotated, List, Tuple

import uvicorn as uvicorn
from fastapi import FastAPI, Depends, Form, File, UploadFile
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from server.component_factory import get_configuration_controller, get_prompt_controller, get_photo_controller, \
    get_existing_playlist_controller, get_request_body_controller
from server.consts.app_consts import PHOTO
from server.controllers.content_controllers.configuration_controller import ConfigurationController
from server.controllers.content_controllers.existing_playlist_controller import ExistingPlaylistController
from server.controllers.content_controllers.photo_controller import PhotoController
from server.controllers.content_controllers.prompt_controller import PromptController
from server.controllers.request_body_controller import RequestBodyController
from server.utils.general_utils import download_database

download_database()
app = FastAPI()
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api/requestBody')
async def request_body(request_body_controller: Annotated[RequestBodyController, Depends(get_request_body_controller)]):
    return await request_body_controller.get()


@app.post('/api/configuration')
async def configuration(request: dict,
                        config_controller: Annotated[ConfigurationController, Depends(get_configuration_controller)]):
    return await config_controller.post(request)


@app.post('/api/prompt')
async def prompt(request: dict, prompt_controller: Annotated[PromptController, Depends(get_prompt_controller)]):
    return await prompt_controller.post(request)


@app.post('/api/photo')
async def photos(photo: Annotated[UploadFile, File()],
                 body: Annotated[str, Form()],
                 photo_controller: Annotated[PhotoController, Depends(get_photo_controller)]):
    request = json.loads(body)
    request[PHOTO] = await photo.read()

    return await photo_controller.post(request)


@app.post('/api/existingPlaylist')
async def existing_playlist(request: dict,
                            existing_playlist_controller: Annotated[ExistingPlaylistController, Depends(get_existing_playlist_controller)]):
    return await existing_playlist_controller.post(request)


app.mount("/", StaticFiles(directory="client/build", html=True), name="static")

if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)
