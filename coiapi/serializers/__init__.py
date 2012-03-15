from flask import json
from pymongo import json_util
import yaml

def json_serialize(data):
    return json.dumps(data, default=json_util.default, sort_keys=True, indent=2)

def yaml_serialize(data=None):
    return yaml.safe_dump(data, default_flow_style=False)

def exhibit_serialize(data=None):
    return None
