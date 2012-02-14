from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask.ext.pymongo import PyMongo
from utils import bson_to_json
from coiapi import create_app

trials_blueprint = Blueprint('trials', __name__)
app = create_app()
mongo = PyMongo(app)

class TrialsAPI(MethodView):
    def _get_trial(self, id=None):
        data = mongo.db[app.config.get('TRIALS_COLL_NAME')].find_one({'_id': id})
        if not data:
            data = {}
        return data

    def _get_trials(self, limit=50, skip=0):
        data = list(mongo.db[app.config.get('TRIALS_COLL_NAME')].find(limit=int(limit),\
            skip=int(skip)))
        if not data:
            data = {}
        return data

    def get(self, id=None):
        # TODO: add case-insensitive lookup
        if id:
            data = self._get_trial(id)
        else:
            data = self._get_trials(limit=request.args.get('limit', 50),\
                skip=request.args.get('offset', 0))
        return bson_to_json(data)

trials_blueprint.add_url_rule('', view_func=TrialsAPI.as_view('trials'), methods=['GET'])
trials_blueprint.add_url_rule('/<id>', view_func=TrialsAPI.as_view('trials'), methods=['GET'])
