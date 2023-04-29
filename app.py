import os
from typing import List

from flask import Flask, jsonify, request, Response
from flask_cors import CORS

from server.env_consts import SPOTIPY_CLIENT_SECRET
from server.logic.openai_adapter import OpenAIAdapter
from server.parameters_transformer import ParametersTransformer
from server.playlists_generator import PlaylistsGenerator
from server.query_condition import QueryCondition

app = Flask(__name__)
app.secret_key = os.environ[SPOTIPY_CLIENT_SECRET]
CORS(app)
playlists_generator = PlaylistsGenerator()
openai_adapter = OpenAIAdapter()


def _generate_response(body: dict, query_conditions: List[QueryCondition]) -> Response:
    access_code = body['accessCode']
    playlist_details = body['playlistDetails']
    playlists_generator.generate(query_conditions, access_code, playlist_details)
    res = {
        'isSuccess': True
    }
    response = jsonify(res)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route("/fromPrompt", methods=['POST'])
def from_prompt() -> Response:
    body = request.get_json()
    query_conditions = ParametersTransformer().transform(body)

    return _generate_response(body, query_conditions)


@app.route("/fromParams", methods=['POST'])
def from_params() -> Response:
    body = request.get_json()
    query_conditions = ParametersTransformer().transform(body)

    return _generate_response(body, query_conditions)


if __name__ == '__main__':
    app.run(debug=True)
