from flask import request, json, g, Response, abort
import redis
import settings
from serializers import json_serialize, yaml_serialize, exhibit_serialize

def redis_connect():
    return redis.Redis(host=settings.REDIS_HOST, \
        port=settings.REDIS_PORT, db=settings.REDIS_DB)

def check_accept_header(accept_header=None):
    # this is called before_request
    accept_types = (
        'application/json',
        'application/yaml',
        'application/exhibit',
    )
    content_type = None
    if accept_header in accept_types:
        content_type = accept_header.split('/')[-1]
    return content_type

def generate_response(request=None, data=None, format=None):
    accept_header = request.headers.get("Accept")
    ctype = format if format else check_accept_header(accept_header)
    serializers = {
        "json": json_serialize,
        "yaml": yaml_serialize,
        "exhibit": exhibit_serialize
    }
    if serializers.has_key(ctype):
        response = serializers[ctype](data)
    else:
        abort(406)
    return Response(response, 200, content_type='application/{0}'.format(ctype))
