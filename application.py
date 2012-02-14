from flask import Flask, request
from flask import jsonify
from flask import g
from flask.views import MethodView
from decorators import throttle
from flask.ext.pymongo import PyMongo
from flask import json
from utils import redis_connect
import utils
import redis
import time
from blueprints.trials import trials_blueprint
from coiapi import create_app

app = create_app()
# blueprints
app.register_blueprint(trials_blueprint, url_prefix='/trials')
mongo = PyMongo(app)
rds = redis_connect()

@app.before_request
def before():
    addr = request.remote_addr
    count = rds.incr('visitors:{0}'.format(addr))
    if count == 1:
        rds.expire('visitors:{0}'.format(addr), 60)
    rds.incr('visits')

class MetricAPI(MethodView):
    #@throttle(rds=rds, limit=10)
    def get(self):
        return jsonify({'visitors': rds.get('visits')})

app.add_url_rule('/visitors', view_func=MetricAPI.as_view('metrics'), methods=['GET'])

if __name__=='__main__':
    app.run(host='0.0.0.0')


