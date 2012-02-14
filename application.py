from flask import Flask, request
from flask import jsonify
from flask import g
from flask.views import MethodView
from decorators import throttle
from flask.ext.pymongo import PyMongo
from flask import json
from utils import redis_connect, bson_to_json
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

class SampleAPI(MethodView):
    #@throttle(rds=rds)
    def get(self, id=None):
        if id:
            data = mongo.db.records.find_one({'r_id': id})
        else:
            data = {}
        return bson_to_json(data)
    
    def post(self):
        r_id = str(int(time.time()))
        data = {
            'r_id': r_id,
            'data': request.form,
        }
        mongo.db.records.insert(data)
        return jsonify({'r_id': r_id})
    
class MetricAPI(MethodView):
    #@throttle(rds=rds, limit=10)
    def get(self):
        return jsonify({'visitors': rds.get('visits')})

app.add_url_rule('/', view_func=SampleAPI.as_view('api'), methods=['GET', 'POST'])
app.add_url_rule('/<id>', view_func=SampleAPI.as_view('api'), methods=['GET'])
app.add_url_rule('/visitors', view_func=MetricAPI.as_view('metrics'), methods=['GET'])

if __name__=='__main__':
    app.run(host='0.0.0.0')


