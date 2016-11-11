from keystoneauth1.identity import v3
from keystoneauth1 import session as k_session
from novaclient import client
# from neutronclient.v2_0 import client as neutron_client
# from cinderclient.v1 import client as cinder_client
import flask
from base import SESSION

class OpenStackClient(object):
    def __init__(self):
        try:
            auth = v3.Password(auth_url='http://192.168.0.12:5000/v3',
                               username="admin",#flask.session['username'],
                               password="1",#flask.session['password'],
                               project_name='admin',
                               user_domain_id='default',
                               project_domain_id='default')
            self.sess = k_session.Session(auth=auth)
        except:
            return str("User not logged in")


class NovaClient(OpenStackClient):
    def __init__(self):
        super(NovaClient, self).__init__()
        self.nova = client.Client("2.1", session=self.sess)

    def check_keystone(self):
        try:
           self.nova.flavors.list()
           return True
        except:
           return False

    def novaflavorlist(self):
            return self.nova.flavors.list()

    def novaimagelist(self):
            return self.nova.images.list()

    def avail_zone_session(self):
           return self.nova.availability_zones.list()

    def novaboot(self):
            image = self.nova.images.find(name=SESSION['image'])#name="cirros-0.3.4-x86_64-uec")
            fl = self.nova.flavors.find(name=SESSION['flavor'])#name="m1.tiny")
            self.nova.servers.create(SESSION['vm_name'], flavor=fl, image=image)

    def nova_vm_list(self):
            return self.nova.servers.list()

    def nova_vm_delete(self):
        instance_list = self.nova.servers.list()
        for ins in instance_list:
                if ins.name == SESSION['vm_delete']:
                    self.nova.servers.delete(ins.id)


class NeutronClient(OpenStackClient):
    def __init__(self):
        super(NeutronClient, self).__init__()
        self.neutron = neutron_client.Client(session=self.sess)

    def networkcreate(self):
        network1 = {'name': SESSION['network_name']}
        self.neutron.create_network({'network': network1})

    def netlist(self):
        network_list = self.neutron.list_networks()
        netlist = []
        temp_list = network_list['networks']
        for i in temp_list:
            for k, v in i.iteritems():
                if str(k)=='name':
                    k1 = '<'+str(k)
                    v1 = str(v)+'>'
                    w = k1+':'+v1
                    netlist.append(w)
        return netlist

    def netdelete(self):
        net_list = self.netlist()
        for network in net_list['networks']:
            for k,v in network.iteritems():
                if str(k)=='name':
                    if str(v) == SESSION['network_name']:
                        break;
            net_id = network['id']
            self.neutron.delete_network(net_id)


class CinderClient(OpenStackClient):
    def __init__(self):
        super(CinderClient, self).__init__()
        self.cinder = cinder_client.Client(session=self.sess)

    def volumelist(self):
        vol_list = self.cinder.volumes.list()
        return vol_list

