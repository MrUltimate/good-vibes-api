import os
import sys
import json
from quart import Quart, jsonify, make_response
from quart_cors import cors

app = Quart(__name__)
app = cors(
    app, allow_origin="http://localhost:3000")
app.config['JSON_SORT_KEYS'] = False

json_data = []


@app.route('/', methods=['GET'])
def start():
    print(sys.path)
    return 'Welcome!', 200


@app.route('/v0/goodvibes/', methods=['GET'])
async def get_reddit_urls():
    with open('data.json') as json_file:
        return jsonify(json.load(json_file)), 200
