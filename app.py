import os

from flask import Flask, request, Response
from flask_cors import CORS

from server.env_consts import SPOTIPY_CLIENT_SECRET
from server.logic.openai_adapter import OpenAIAdapter
from server.parameters_transformer import ParametersTransformer
from server.utils import generate_response

app = Flask(__name__)
app.secret_key = os.environ[SPOTIPY_CLIENT_SECRET]
CORS(app)
openai_adapter = OpenAIAdapter()


@app.route("/fromPrompt", methods=['POST'])
def from_prompt() -> Response:
    body = request.get_json()
    user_text = body['playlistDetails']['prompt']
    query_conditions = openai_adapter.generate_query_conditions(user_text)

    return generate_response(body, query_conditions)


@app.route("/fromParams", methods=['POST'])
def from_params() -> Response:
    body = request.get_json()
    query_conditions = ParametersTransformer().transform(body)

    return generate_response(body, query_conditions)


if __name__ == '__main__':
    app.run(debug=True)
