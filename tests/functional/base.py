from api import app

import unittest


class TestBase(unittest.TestCase):
    def setUp(self):
        # create a test client
        self.client = app.test_client()
        self.client.testing = True

    def tearDown(self):
        pass

    # helper methods
    def login(self, username, password):
        return self.client.post('/login',
                                data=dict(username=username,
                                          password=password),
                                follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', content_type='html/text',
                               follow_redirects=True)
