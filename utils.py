import redis
import settings
from flask import json
from pymongo import json_util

def bson_to_json(data):
    return json.dumps(data, default=json_util.default, sort_keys=True, indent=2)

def redis_connect():
    return redis.Redis(host=settings.REDIS_HOST, \
        port=settings.REDIS_PORT, db=settings.REDIS_DB)

