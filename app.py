#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, url_for
import urllib
import json


app = Flask(__name__, static_url_path="")


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# load ids & descriptions from JSON CPV vocabulary
descriptions = json.loads(urllib.urlopen("files/main_vocabulary.json").read())


def make_public_cpv(cpv):
    new_cpv = {}
    for field in cpv:
        if field == 'id':
            new_cpv['uri'] = url_for('get_cpv', cpv_id=cpv['id'], _external=True)
        else:
            new_cpv[field] = cpv[field]
    return new_cpv


@app.route('/api/v1/descriptions', methods=['GET'])
def get_descriptions():
    return jsonify({'descriptions': map(make_public_cpv, descriptions)})


@app.route('/api/v1/description/<int:cpv_id>', methods=['GET'])
def get_cpv(cpv_id):
    cpv = filter(lambda t: t['id'] == cpv_id, descriptions)
    if len(cpv) == 0:
        abort(404)
    return jsonify({'cpv': make_public_cpv(cpv[0])})

if __name__ == '__main__':
    app.run(debug=True)
