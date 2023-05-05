import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from server.app_resources.configuration_resource import Configuration
from server.app_resources.min_max_values_resource import MinMaxValues
from server.app_resources.possible_values_resource import PossibleValues
from server.app_resources.prompt_resource import Prompt
from server.consts.env_consts import SPOTIPY_CLIENT_SECRET
from server.logic.openai_adapter import OpenAIAdapter

app = Flask(__name__)
app.secret_key = os.environ[SPOTIPY_CLIENT_SECRET]
CORS(app)
api = Api(app)
openai_adapter = OpenAIAdapter()


api.add_resource(Configuration, '/api/configuration')
api.add_resource(Prompt, '/api/prompt')
api.add_resource(MinMaxValues, '/api/minMaxValues/<string:column_name>')
api.add_resource(PossibleValues, '/api/possibleValues/<string:column_name>')


if __name__ == '__main__':
    app.run(debug=True)
