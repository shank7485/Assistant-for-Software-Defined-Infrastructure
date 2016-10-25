from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient import client
auth = v3.Password(auth_url='http://example.com:5000/v3',
                   username='username',
                   password='password',
                   project_name='project-name',
                   user_domain_id='default',
                   project_domain_id='default')
sess = session.Session(auth=auth)
nova = client.Client("2.1", session=sess)
nova.flavors.list()
nova.servers.list()
nova.keypairs.list()


class OpenStackClient(object):
    def __init__(self, username, password, URL):
        self.username = username
        self.password = password
        self.URL = URL

    def create_vm_session(self):
        # TODO
        pass

    def list_vm_session(self):
        # TODO
        pass