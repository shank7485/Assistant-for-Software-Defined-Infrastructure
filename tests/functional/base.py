from api import app

import unittest


class TestBase(unittest.TestCase):
    def setUp(self):
        # create a test client
        self.client = app.test_client()
        self.client.testing = True

    def tearDown(self):
        pass