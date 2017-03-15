import json
import unittest

import base


class TestAPI(base.TestBase):
    def setUp(self):
        super(TestAPI, self).setUp()

    def test_login_endpoint(self):
        # Check the content of the response by hitting the /login endpoint
        response = self.client.get('/login')
        self.assertIn(
            ' If you are not sure which  authentication method to use,'
            ' contact your administrator',
            response.data)

    def test_correct_login(self):
        # Check if the login works with correct credentials
        response = self.client.post('/login', data=dict(username='admin',
                                                        password='secrete'),
                                    follow_redirects=True)
        self.assertIn('Send', response.data)
        self.assertIn('Openstack Assistant',
                      response.data)

    def test_incorrect_login(self):
        # Check if the login fails with incorrect credentials
        response = self.client.post('/login', data=dict(username='xyz',
                                                        password='xyz'),
                                    follow_redirects=True)
        self.assertIn('Invalid Username/Password', response.data)

    def test_correct_logout(self):
        # send HTTP GET request to the application on the logout page
        # to check whether it redirects the request to the login page
        response = self.client.get('/logout', content_type='html/text')
        self.assertIn('Redirecting', response.data)
        self.assertIn(
            'You should be redirected automatically to target URL',
            response.data)

    def test_chat_api(self):
        self.login('admin', 'secrete')
        res = self.client.get('/chat?question=Hi',
                              content_type='html/text')
        response = json.loads(res.data)
        msg = response.get('message')
        self.assertIn('Hello', msg)
        self.logout()

    def test_list_vms(self):
        self.login('admin', 'secrete')
        res = self.client.get('/chat?question=list vms',
                              content_type='html/text')
        response = json.loads(res.data)
        msg = response.get('message')
        self.assertIn('Virtual Machines', msg)
        self.logout()

    def test_list_networks(self):
        self.login('admin', 'secrete')
        response = self.client.get('/chat?question=list nets',
                                   content_type='html/text')
        self.assertIn('public',
                      response.data)
        self.assertIn('private',
                      response.data)
        self.logout()

    def test_list_volumes(self):
        self.login('admin', 'secrete')
        res = self.client.get('/chat?question=list volumes',
                              content_type='html/text')
        response = json.loads(res.data)
        msg = response.get('message')
        self.assertIn('Here is the list of available volumes', msg)
        self.logout()

    def test_create_vm(self):
        self.create_test_vm('Test_VM_2')
        self.login('admin', 'secrete')
        res = self.client.get('/chat?question=list vms')
        response = json.loads(res.data)
        vm_list = response.get('list')
        vm_value = filter(lambda vm: vm['value'] == 'Test_VM_2', vm_list)
        self.assertEqual('Test_VM_2', vm_value[0].get('value'))
        self.logout()
        # TODO(ndahiwade): Add Cleanup, otherwise resources will keep
        #  getting created

    # TODO(ndahiwade): Add other API endpoints to this

if __name__ == '__main__':
    unittest.main()
