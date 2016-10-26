from keystoneauth1.identity import v3
from keystoneauth1 import session as k_session
from novaclient import client
import flask


class OpenStackClient(object):
    def __init__(self):
        auth = v3.Password(auth_url='http://192.168.0.179:5000/v3',
                           username='admin',
                           password='secret',
                           project_name='admin',
                           user_domain_id='default',
                           project_domain_id='default')
        self.sess = k_session.Session(auth=auth)

    def check_keystone(self):
        try:
            nova = client.Client("2.1", session=self.sess)
            if (nova.flavors.list()):
                return True
        except:
            return False

    def novaflavorlist(self):
        try:
            nova = client.Client("2.1", session=self.sess)
            return str(nova.flavors.list())
        except:
            return str("User not logged in")

    def novaimagelist(self):
        try:
            nova = client.Client("2.1", session=self.sess)
            return str(nova.images.list())
        except:
            return str("User not logged in")

    def avail_zone_session(self):
       try:
           nova = client.Client("2.1", session=self.sess)
           return str(nova.availability_zones.list())
       except:
           return str("User not logged in")

    def novaboot(self):
        try:
            nova = client.Client("2.1", session=self.sess)
            image = nova.images.find(name=flask.session['image'])#name="cirros-0.3.4-x86_64-uec")
            fl = nova.flavors.find(name=flask.session['flavor'])#name="m1.tiny")
            nova.servers.create(flask.session['name'], flavor=fl, image=image)
        except:
            return str("User not logged in")

    def list_vm_session(self):
        # TODO
        pass
