from keystoneauth1.identity import v3
from keystoneauth1 import session as k_session
from novaclient import client
from neutronclient.v2_0 import client as neutron_client
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


class NovaClient(OpenStackClient):
    def __init__(self):
        super(NovaClient).__init__()
        self.nova = client.Client("2.1", session=self.sess)

    def check_keystone(self):
        try:
            if (self.nova.flavors.list()):
                return True
        except:
            return False

    def novaflavorlist(self):
        try:
            return str(self.nova.flavors.list())
        except:
            return str("User not logged in")

    def novaimagelist(self):
        try:
            return str(self.nova.images.list())
        except:
            return str("User not logged in")

    def avail_zone_session(self):
       try:
           return str(self.nova.availability_zones.list())
       except:
           return str("User not logged in")

    def novaboot(self):
        try:
            image = self.nova.images.find(name=flask.session['image'])#name="cirros-0.3.4-x86_64-uec")
            fl = self.nova.flavors.find(name=flask.session['flavor'])#name="m1.tiny")
            self.nova.servers.create(flask.session['name'], flavor=fl, image=image)
        except:
            return str("User not logged in")

    def nova_vm_list(self):
        try:
            self.nova.servers.list()
        except:
            return str("User bot loggin in")


class NeutronClient(OpenStackClient):
    def __init__(self):
        super(NeutronClient).__init__()
        self.neutron = neutron_client.Client(session=self.sess)

    def networkcreate(self):
        try:
            network1 = {'name': flask.session['network_name']}
            self.neutron.create_network({'network': network1})
        except:
            return str("User not logged in")

    def netlist(self):
        try:
            list = self.neutron.list_networks(name = flask.session['network_name'])
            return str(list)
        except:
            return str("User not logged in")
