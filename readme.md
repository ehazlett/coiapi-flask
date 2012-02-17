COI API
===========
This is a simple Flask (http://flask.pocoo.org) application demonstrating exposing a MongoDB backed API.  The application will store and retrieve data from MongoDB as well as perform simple IP-based throttling (configurable via a decorator).

Setup
------
* Create virtualenv (`mkvirtualenv coiapi` or `virtualenv --no-site-packages coiapi`)
* Activate virtualenv and install requirements: `pip install -r requirements.txt`
* Start MongoDB and Redis (application uses default ports and db #12 for redis)
* Start app: `python application.py`
* Application should now be running on `0.0.0.0:5000`

Usage
------

Insert data to MongoDB:

    curl -v -d "test=123&moretesting=456" localhost:5000/

You will get a response (in JSON) like:

    {
      "r_id": "1329142610"
    }

Retrieve data from MongoDB:

    curl localhost:5000/1329142610

You will get a response (in JSON) like:
        
    {
      "_id": {"$oid": "4f391b52db487d114b000001"}, 
      "data": {"moretesting": ["456"], 
      "test": ["123"]}, 
      "r_id": "1329142610"
    }


Throttling
----------
To test throttling, simply perform a series of requests against the throttled url.  By default, the `/` url is limited to 50 req/20 sec and the `/visitors` url is limited to 10 req/20 sec.

    curl localhost:5000/visitors    (x15 in under 20 seconds)

You will get a response (in JSON) like:

    {
      "status": "fail", 
      "response": "Over limit ; try again later"
    }


Tests
-----
There are some basic default tests in `tests.py`.  One performs a simple request on the `/` url, checking for HTTP status code.  The other performs a request on `/visitors` checking content.

To run the tests:

    python tests.py -v


