from flask import Flask, jsonify, request
from flask_cors import CORS

from server.playlists_generator import PlaylistsGenerator

app = Flask(__name__)
CORS(app)
playlists_generator = PlaylistsGenerator()


@app.route("/fromPrompt", methods=['POST'])
def from_prompt():
    print('bla')


@app.route("/fromParams", methods=['POST'])
def from_params():
    playlists_generator.generate([], '')
    res = {
        'isSuccess': True
    }
    print('bla')
    response = jsonify(res)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == '__main__':
    app.run(debug=True)
