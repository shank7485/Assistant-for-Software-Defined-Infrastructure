import os
import unittest

from api import app


class TestBase(unittest.TestCase):

    # NOTE(ndahiwade): Kindly source the OpenStack credentials before
    # running the tests so that the environment variables are set for the
    # username and password.
    username = os.environ['OS_USERNAME']
    password = os.environ['OS_PASSWORD']
    default_flavor = 'm1.tiny'
    default_image = 'cirros-0.3.4-x86_64-uec'
    default_network = 'private'

    def setUp(self):
        # create a test client
        self.client = app.test_client()
        self.client.testing = True

    def tearDown(self):
        pass

    # Helper methods for API testing.
    def login(self):
        return self.client.post('/login',
                                data=dict(username=self.username,
                                          password=self.password),
                                follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', content_type='html/text',
                               follow_redirects=True)

    def create_test_vm(self, vm_name):
        self.login()
        self.client.get('/chat?question=create vm',
                        content_type='html/text')
        self.client.get('/set?key=flavor&value=' + self.default_flavor)
        self.client.get('/set?key=image&value=' + self.default_image)
        self.client.get('/set?key=vm_name&value=' + vm_name)
        self.client.get('/set?key=net_name&value=' + self.default_network)
        self.client.get('/set?key=vm_create_confirm&value=yes')
        self.client.get('/set?key=vm_create_confirm&value=yes')
        self.logout()

    def delete_test_vm(self, vm_name):
        self.login()
        self.client.get('/chat?question=delete vm',
                        content_type='html/text')
        self.client.get('/set?key=vm_delete&value=' + vm_name)
        self.client.get('/set?key=vm_delete_confirm&value=yes')
        self.logout()

    def create_test_network(self, net_name, subnet_name, cidr):
        self.login()
        self.client.get('/chat?question=create network',
                        content_type='html/text')
        self.client.get('/set?key=network_name&value=' + net_name)
        self.client.get('/set?key=subnet_name&value=' + subnet_name)
        self.client.get('/set?key=cidr&value=' + cidr)
        self.client.get('/set?key=network_create_confirm&value=yes')
        self.logout()

    def delete_test_network(self, net_name):
        self.login()
        self.client.get('/chat?question=delete network',
                        content_type='html/text')
        self.client.get('/set?key=network_delete&value=' + net_name)
        self.client.get('/set?key=network_delete_confirm&value=yes')
        self.logout()