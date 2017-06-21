import logging
import json

from flask import Flask, jsonify, request, abort, Response

from docker import Client

import helpers

from config import parse_config


log = logging.getLogger('pratai-docker')
app = Flask(__name__)


cli = Client(base_url='tcp://127.0.0.1:4243', tls=False, version='1.18')


@app.before_request
def keystone():
    # return unauthorized()
    # once this is allowed, we still to validate the access to individual
    # resources in each function
    if request.endpoint == 'function_execute':
        # print('skip validation?')
        # should the cleaning needs to happen here?
        pass
    else:
        # this should be replaced by keystone middleware
        #if not request.headers.get('X-User-ID', None) \
        #        and not request.headers.get('X-Tenant-ID'):
        #    return unauthorized()
        pass


@app.errorhandler(400)
def bad_request(error=""):
    message = {
            'status_code': 400,
            'message': 'Bad Request: {0}'.format(error),
    }
    log.error(error)
    resp = jsonify(message)
    resp.status_code = 400
    return resp


@app.errorhandler(404)
def not_found(error=""):
    message = {
            'status_code': 404,
            'message': 'Not Found: ' + request.url,
    }
    log.error(error)
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.errorhandler(401)
def unauthorized(error=""):
    message = {
            'status_code': 401,
            'message': 'Unauthorized',
    }
    log.error(error)
    resp = jsonify(message)
    resp.status_code = 401
    return resp


@app.errorhandler(405)
def method_not_allowed(error=""):
    message = {
            'status_code': 405,
            'message': 'Method Not Allowed',
    }
    log.error(error)
    resp = jsonify(message)
    resp.status_code = 405
    return resp


@app.errorhandler(500)
def critical_error(error=""):
    message = {
            'status_code': 500,
            'message': error,
    }
    log.error(error)
    resp = jsonify(message)
    resp.status_code = 500
    return resp


@app.route('/', methods=['GET'])
def discovery():
    # show all the endpoints
    endpoints = {
        "/": "GET",
        "v1/images": "GET",
        "v1/images/{image_id}": "DELETE",
    }
    return jsonify(endpoints)


# images

@app.route('/containers', methods=['GET'])
def container_list():
    return jsonify(cli.containers())


@app.route('/images', methods=['GET'])
def images_get():
    return jsonify(cli.images())


@app.route('/images/<image_id>', methods=['DELETE'])
def delete_image(image_id):
    return helpers.delete(image_id)


@app.route('/images/build', methods=['POST'])
def image_build():
    req = json.loads(request.data)
    out = helpers.build(req)

    _id = None
    for line in out.splitlines():
        if 'Successfully built' in line:
            _id = line.split()[2]

    resp = jsonify({'image_id': _id})
    resp.status_code = 201
    return resp


@app.route('/container/<container_id>/kill', methods=['POST'])
def container_kill(container_id):
    return helpers.kill(container_id)


if __name__ == '__main__':
    app.run(host=parse_config("api")['url'],
            port=int(parse_config("api")['port']),
            debug=True)
