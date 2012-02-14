from flask import json
from pymongo import json_util

def json_serialize(data):
    return json.dumps(data, default=json_util.default, sort_keys=True, indent=2)

