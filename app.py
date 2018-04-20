#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, url_for
import urllib
import json
import requests
import os

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

app = Flask(__name__, static_url_path="")

host = 'search-cpv-hs-staging-ctnuutdqpqmvmr5nlojjungtda.eu-west-1.es.amazonaws.com'
awsauth = AWS4Auth(os.getenv('AWS_ACCESS_KEY_ID'), os.getenv('AWS_SECRET_ACCESS_KEY'), 'eu-west-1', 'es')

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# load ids & descriptions from JSON CPV vocabulary
cpv_descriptions = json.loads(urllib.urlopen("files/main_vocabulary.json").read())


def make_public_json(cpv):
    new_cpv = {}
    for field in cpv:
        if field == 'id':
            new_cpv['id'] = cpv['id']
            new_cpv['uri'] = url_for('get_cpv', cpv_id=cpv['id'], _external=True)
        else:
            new_cpv[field] = cpv[field]
    return new_cpv


@app.route('/api/v1/cpvs', methods=['GET'])
def get_descriptions():
    return jsonify({'descriptions': map(make_public_json, cpv_descriptions)})

@app.route('/api/v1/hs/<int:hs_id>', methods=['GET'])
def get_hs(hs_id):
    hs = es.search(index="hs_codes", q=int(hs_id))

    if len(hs) == 0:
        abort(404)

    res = es.search(index="cpv_codes", q=hs['hits']['hits'][0]['_source']['description'])

    first_result = res['hits']['hits'][0]
    hs_description = first_result['_source']['text']
    hs_id = first_result['_source']['id']

    return jsonify({'cpv': make_public_json(hs[0]), 'hs': {'description': hs_description, 'id': hs_id}})


@app.route('/api/v1/cpv/<int:cpv_id>', methods=['GET'])
def get_cpv(cpv_id):
    cpv = filter(lambda t: t['id'] == cpv_id, cpv_descriptions)
    if len(cpv) == 0:
        abort(404)

    res = es.search(index="hs_codes", q=cpv[0]['description'])

    first_result = res['hits']['hits'][0]
    hs_description = first_result['_source']['text']
    hs_id = first_result['_source']['id']

    return jsonify({'cpv': make_public_json(cpv[0]), 'hs': {'description': hs_description, 'id': hs_id}})

if __name__ == '__main__':
    app.run(debug=True)
