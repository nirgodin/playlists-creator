from aiohttp import ClientSession
from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin

from server.component_factory import get_configuration_controller, get_prompt_controller, get_photo_controller, \
    get_existing_playlist_controller, get_request_body_controller
from server.utils.general_utils import download_database

download_database()
app = Flask(__name__, static_folder='client/build', static_url_path='')
CORS(app)
session = ClientSession()


@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/requestBody', methods=['GET'])
async def request_body():
    request_body_controller = await get_request_body_controller()
    return await request_body_controller.get()


@app.route('/api/configuration', methods=['POST'])
async def configuration():
    configuration_controller = await get_configuration_controller()
    return await configuration_controller.post()


@app.route('/api/prompt', methods=['POST'])
async def prompt():
    prompt_controller = await get_prompt_controller()
    return await prompt_controller.post()


@app.route('/api/photo', methods=['POST'])
async def photo():
    photo_controller = await get_photo_controller()
    return await photo_controller.post()


@app.route('/api/existingPlaylist', methods=['POST'])
async def existing_playlist():
    existing_playlist_controller = await get_existing_playlist_controller()
    return await existing_playlist_controller.post()


if __name__ == '__main__':
    app.run(debug=False)
