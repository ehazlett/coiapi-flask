#!/usr/bin/env python
import application
import unittest
import utils
from werkzeug.test import create_environ
from flask import json, request, Request

def get_app():
    return application.app.test_client()

class CoreTestCase(unittest.TestCase):
    def setUp(self):
        self.app = get_app()

    def tearDown(self):
        pass

    def test_visitors(self):
        rv = self.app.get('/visitors')
        data = json.loads(rv.data)
        assert data.has_key('visitors')

class TrialsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = get_app()

class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = get_app()
    
    def test_check_content_type_json(self):
        hdr = 'application/json'
        self.assertEqual(utils.check_accept_header(hdr), 'json')

    def test_check_content_type_foo(self):
        hdr = 'application/foo'
        self.assertEqual(utils.check_accept_header(hdr), None)
    
    def test_generate_response_with_only_accept_header(self):
        env = create_environ(headers={'Accept': 'application/json'})
        req = Request(env)
        resp = utils.generate_response(request=req)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(resp.content_type, 'application/json')
        #TODO: check the serializing?

    def test_generate_response_with_only_bad_accept_header(self):
        env = create_environ(headers={'Accept': 'applictation/blah'})
        req = Request(env)
        resp = utils.generate_response(request=req)
        self.assertEqual(resp.status_code, 406)
        self.assertEqual(resp.status, '406 NOT ACCEPTABLE')

    def test_generate_response_with_only_extension(self):
        env = create_environ()
        req = Request(env)
        resp = utils.generate_response(request=req, data=None, \
            format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(resp.content_type, 'application/json')

    def test_generate_response_with_header_and_extension_same_and_valid(self):
        env = create_environ(headers={'Accept': 'application/json'})
        req = Request(env)
        resp = utils.generate_response(request=req, data=None, \
            format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(resp.content_type, 'application/json')

    def test_generate_response_with_header_and_extension_different_and_valid(self):
        env = create_environ(headers={'Accept': 'application/yaml'})
        req = Request(env)
        resp = utils.generate_response(request=req, data=None, \
            format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(resp.content_type, 'application/json')

    def test_generate_response_with_invalid_header_and_valid_extension(self):
        env = create_environ(headers={'Accept': 'application/foo'})
        req = Request(env)
        resp = utils.generate_response(request=req, data=None, \
            format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(resp.content_type, 'application/json')

    def test_generate_response_with_valid_header_and_invalid_extension(self):
        env = create_environ(headers={'Accept': 'application/json'})
        req = Request(env)
        resp = utils.generate_response(request=req, data=None, \
            format='foo')
        self.assertEqual(resp.status_code, 406)
        self.assertEqual(resp.status, '406 NOT ACCEPTABLE')

if __name__=='__main__':
    unittest.main()
