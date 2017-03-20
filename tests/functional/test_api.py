import json
import unittest

import base


class TestAPI(base.TestBase):
    def setUp(self):
        super(TestAPI, self).setUp()

    def test_login_endpoint(self):
        """ Check the content of the response by hitting the
        /login endpoint. """
        response = self.client.get('/login')
        self.assertIn(
            ' If you are not sure which  authentication method to use,'
            ' contact your administrator',
            response.data)

    def test_correct_login(self):
        """ Check if the login works with correct credentials. """
        response = self.client.post('/login',
                                    data=dict(username=self.username,
                                              password=self.password),
                                    follow_redirects=True)
        self.assertIn('Send', response.data)
        self.assertIn('Openstack Assistant',
                      response.data)

    def test_incorrect_login(self):
        """ Check if the login fails with incorrect credentials. """
        response = self.client.post('/login', data=dict(username='xyz',
                                                        password='xyz'),
                                    follow_redirects=True)
        self.assertIn('Invalid Username/Password', response.data)

    def test_correct_logout(self):
        """ send HTTP GET request to the application on the logout page
        to check whether it redirects the request to the login page. """
        response = self.client.get('/logout', content_type='html/text')
        self.assertIn('Redirecting', response.data)
        self.assertIn(
            'You should be redirected automatically to target URL',
            response.data)

    def test_chat_api(self):
        """ Testing chat api with the response message. """
        self.login()
        res = self.client.get('/chat?question=Hi',
                              content_type='html/text')
        response = json.loads(res.data)
        msg = response.get('message')
        self.assertIn('Hello', msg)
        self.logout()

    def test_list_vms(self):
        """ Testing listing VMs with the response message. """
        self.login()
        res = self.client.get('/chat?question=list vms',
                              content_type='html/text')
        response = json.loads(res.data)
        msg = response.get('message')
        if response.get('list')==None:
            self.assertIn('No VMs', msg)
        else:
            self.assertIn('Virtual Machines', msg)
        self.logout()

    def test_list_networks(self):
        """ Test listing network with public and private being
        default networks. """
        self.login()
        response = self.client.get('/chat?question=list nets',
                                   content_type='html/text')
        self.assertIn('public',
                      response.data)
        self.assertIn('private',
                      response.data)
        self.logout()

    def test_list_volumes(self):
        """ Test listing volumes with the response message. """
        self.login()
        res = self.client.get('/chat?question=list volumes',
                              content_type='html/text')
        response = json.loads(res.data)
        msg = response.get('message')
        self.assertIn('Here is the list of available volumes', msg)
        self.logout()

    def test_create_vm(self):
        """ Testing Creating, Listing and Deleting a VM. """
        self.create_test_vm('Test_VM_2')
        self.login()
        res = self.client.get('/chat?question=list vms')
        response = json.loads(res.data)
        vm_list = response.get('list')
        vm_value = filter(lambda vm: vm['value'] == 'Test_VM_2', vm_list)
        self.assertEqual('Test_VM_2', vm_value[0].get('value'))
        self.logout()
        # Clean up
        self.delete_test_vm('Test_VM_2')

    def test_create_network(self):
        """ Testing Creating, Listing and Deleting Network. """
        self.create_test_network('Test_Net_2', 'Test_Subnet_2',
                                 '10.10.1.0/24')
        self.login()
        res = self.client.get('/chat?question=list networks')
        response = json.loads(res.data)
        net_list = response.get('list')
        net_value = filter(lambda net: net['value'] == 'Test_Net_2', net_list)
        self.assertEqual('Test_Net_2', net_value[0].get('value'))
        self.logout()
        # Clean up
        self.delete_test_network('Test_Net_2')

    # TODO(ndahiwade): Add other API tests to this

if __name__ == '__main__':
    unittest.main()
