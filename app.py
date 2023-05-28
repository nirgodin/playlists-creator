import os

from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin
from flask_restful import Api

from server.consts.env_consts import SPOTIPY_CLIENT_SECRET
from server.controllers.content_controllers.configuration_controller import ConfigurationController
from server.controllers.content_controllers.photo_controller import PhotoController
from server.controllers.content_controllers.prompt_controller import PromptController
from server.controllers.features_descriptions_controller import FeaturesDescriptionsController
from server.controllers.features_names_controller import FeaturesNamesController
from server.controllers.min_max_values_controller import MinMaxValuesController
from server.controllers.possible_values_controller import PossibleValuesController
from server.controllers.request_body_controller import RequestBodyController
from server.utils import download_database

download_database()
app = Flask(__name__, static_folder='client/build', static_url_path='')
app.secret_key = os.environ[SPOTIPY_CLIENT_SECRET]
CORS(app)
api = Api(app, decorators=[cross_origin()])


@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


api.add_resource(ConfigurationController, '/api/configuration')
api.add_resource(PromptController, '/api/prompt')
api.add_resource(PhotoController, '/api/photo')
api.add_resource(MinMaxValuesController, '/api/minMaxValues/<string:column_name>')
api.add_resource(PossibleValuesController, '/api/possibleValues/<string:column_name>')
api.add_resource(RequestBodyController, '/api/requestBody')
api.add_resource(FeaturesNamesController, '/api/featuresNames/<string:feature_type>')
api.add_resource(FeaturesDescriptionsController, '/api/featuresDescriptions')

if __name__ == '__main__':
    app.run(debug=False)

