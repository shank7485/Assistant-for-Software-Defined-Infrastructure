from api import app

import unittest


class TestBase(unittest.TestCase):

    default_flavor = 'm1.tiny'
    default_image = 'cirros-0.3.4-x86_64-uec'
    default_network = 'private'

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

    def create_test_vm(self, vm_name):
        self.login('admin', 'secrete')
        self.client.get('/chat?question=create vm',
                        content_type='html/text')
        self.client.get('/set?key=flavor&value='+self.default_flavor)
        self.client.get('/set?key=image&value=' + self.default_image)
        self.client.get('/set?key=vm_name&value=' + vm_name)
        self.client.get('/set?key=net_name&value=' + self.default_network)
        self.client.get('/set?key=vm_create_confirm&value=yes')
        self.client.get('/set?key=vm_create_confirm&value=yes')
        self.logout()
