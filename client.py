from keystoneauth1.identity import v3
from keystoneauth1 import session as k_session
from novaclient import client
import flask


class OpenStackClient(object):
    def check_keystone(self):
        try:
            auth = v3.Password(auth_url='http://172.99.106.120:5000/v3',
                               username=flask.session['username'],
                               password=flask.session['password'],
                               project_name='admin',
                               user_domain_id='default',
                               project_domain_id='default')
            sess = k_session.Session(auth=auth)
            nova = client.Client("2.1", session=sess)
            if (nova.flavors.list()):
                return True
        except:
            return False

    def create_vm_session(self):
        # TODO
        pass

    def list_vm_session(self):
        # TODO
        pass