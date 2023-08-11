from aiohttp import ClientSession
from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin

from server.controllers.content_controllers.configuration_controller import ConfigurationController
from server.controllers.content_controllers.existing_playlist_controller import ExistingPlaylistController
from server.controllers.content_controllers.photo_controller import PhotoController
from server.controllers.content_controllers.prompt_controller import PromptController
from server.controllers.request_body_controller import RequestBodyController
from server.utils.general_utils import download_database

download_database()
app = Flask(__name__, static_folder='client/build', static_url_path='')
CORS(app)
session = ClientSession()
request_body_controller = RequestBodyController()
configuration_controller = ConfigurationController(session)
prompt_controller = PromptController(session)
photo_controller = PhotoController(session)
existing_playlist_controller = ExistingPlaylistController(session)


@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/requestBody', methods=['GET'])
async def request_body():
    return await request_body_controller.get()


@app.route('/api/configuration', methods=['POST'])
async def configuration():
    return await configuration_controller.post()


@app.route('/api/prompt', methods=['POST'])
async def prompt():
    return await prompt_controller.post()


@app.route('/api/photo', methods=['POST'])
async def photo():
    return await photo_controller.post()


@app.route('/api/existingPlaylist', methods=['POST'])
async def existing_playlist():
    return await existing_playlist_controller.post()


if __name__ == '__main__':
    app.run(debug=False)
