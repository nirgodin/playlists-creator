from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/fromPrompt", methods=['POST'])
def from_prompt():
    print('bla')


@app.route("/fromParams", methods=['POST'])
def from_params():
    res = {
        'isSuccess': True
    }
    print('bla')
    response = jsonify(res)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == '__main__':
    app.run(debug=True)
