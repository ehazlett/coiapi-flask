#!/usr/bin/env python
import application
import unittest
from flask import json

class CoreTestCase(unittest.TestCase):
    def setUp(self):
        self.app = application.app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        rv = self.app.get('/')
        assert rv.status_code == 200

    def test_visitors(self):
        rv = self.app.get('/visitors')
        data = json.loads(rv.data)
        assert data.has_key('visitors')

if __name__=='__main__':
    unittest.main()
