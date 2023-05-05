import os

from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin
from flask_restful import Api

from server.app_resources.configuration_resource import Configuration
from server.app_resources.min_max_values_resource import MinMaxValues
from server.app_resources.possible_values_resource import PossibleValues
from server.app_resources.prompt_resource import Prompt
from server.consts.env_consts import SPOTIPY_CLIENT_SECRET

app = Flask(__name__, static_folder='client/build', static_url_path='')
app.secret_key = os.environ[SPOTIPY_CLIENT_SECRET]
CORS(app)
api = Api(app, decorators=[cross_origin()])


@app.route('/api', methods=['GET'])
@cross_origin()
def index():
    return {
        'Hey': 'It\'s working!'
    }


@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


api.add_resource(Configuration, '/api/configuration')
api.add_resource(Prompt, '/api/prompt')
api.add_resource(MinMaxValues, '/api/minMaxValues/<string:column_name>')
api.add_resource(PossibleValues, '/api/possibleValues/<string:column_name>')


if __name__ == '__main__':
    app.run(debug=False)
