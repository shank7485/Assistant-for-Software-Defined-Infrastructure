from keystoneauth1.identity import v3
from keystoneauth1 import session as k_session
from novaclient import client
from neutronclient.v2_0 import client as neutron_client
from cinderclient.v1 import client as cinder_client
from sessions_file import SESSION
import os
from oslo_config import cfg

CREDENTIALS = {}


class ReadConfig(object):
    def __init__(self, conf_path):
        self.conf_path = conf_path

        self.opt_group = cfg.OptGroup(name='endpoint',
                                 title='Get the endpoints for keystone')

        self.endpoint_opts = [cfg.StrOpt('endpoint', default='None',
            help=('URL or IP address where OpenStack keystone runs.'))
        ]

        CONF = cfg.CONF
        CONF.register_group(self.opt_group)
        CONF.register_opts(self.endpoint_opts, self.opt_group)

        CONF(default_config_files=[self.conf_path])
        self.AUTH_ENDPOINT = CONF.endpoint.endpoint

    def get_endpoint(self):
        return self.AUTH_ENDPOINT


class OpenStackClient(object):
    def __init__(self):
        self.endpoint_IP = ReadConfig('app.conf').get_endpoint()
        self.endpoint = 'http://' + self.endpoint_IP + ':5000/v3'

    def keystone_auth(self, username, password):
        try:
           auth = v3.Password(auth_url=self.endpoint,
                               username=username,
                               password=password,
                               project_name='admin',
                               user_domain_id='default',
                               project_domain_id='default')
           self.sess = k_session.Session(auth=auth)
           CREDENTIALS[username] = password
           return True
        except:
           return False


class NovaClient(OpenStackClient):
    def __init__(self):
        super(NovaClient, self).__init__()
        auth = v3.Password(auth_url=self.endpoint,
                           username=CREDENTIALS.keys()[0],
                           password=CREDENTIALS[CREDENTIALS.keys()[0]],
                           project_name='admin',
                           user_domain_id='default',
                           project_domain_id='default')
        self.sess = k_session.Session(auth=auth)
        self.nova = client.Client("2.1", session=self.sess)
        #self.neutron = neutron_client.Client(session=self.sess)

    def novaflavorlist(self):
            return self.nova.flavors.list()

    def novaimagelist(self):
            return self.nova.images.list()

    def avail_zone_session(self):
           return self.nova.availability_zones.list()

    def novaboot(self):
            image = self.nova.images.find(name=SESSION['image'])
            fl = self.nova.flavors.find(name=SESSION['flavor'])
            #net_name = self.nova.networks.find(label=SESSION['net_name'])
            #import pdb; pdb.set_trace()
            net_list = self.nova.networks.list()
            for network in net_list:
                if network.label == SESSION['net_name']:
                    net_id = network.id
            self.nova.servers.create(SESSION['vm_name'], flavor=fl,
                                     image=image, nics=[{'net-id': net_id}])

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
        auth = v3.Password(auth_url=self.endpoint,
                           username=CREDENTIALS.keys()[0],
                           password=CREDENTIALS[CREDENTIALS.keys()[0]],
                           project_name='admin',
                           user_domain_id='default',
                           project_domain_id='default')
        self.sess = k_session.Session(auth=auth)
        self.neutron = neutron_client.Client(session=self.sess)

    def networkcreate(self):
        network1 = {'name': SESSION['network_name']}
        net = self.neutron.create_network({'network': network1})
        net_id = net['network']['id']
        subnet1 = {'name': SESSION['subnet_name'], "ip_version": 4,
                   'network_id': net_id, 'cidr': SESSION['cidr']}
        self.neutron.create_subnet({'subnet': subnet1})

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
        net_list = self.neutron.list_networks()
        for network in net_list['networks']:
            if network['name'] == SESSION['network_delete']:
                net_id = network['id']
                self.neutron.delete_network(net_id)

class CinderClient(OpenStackClient):
    def __init__(self):
        super(CinderClient, self).__init__()
        auth = v3.Password(auth_url=self.endpoint,
                           username=CREDENTIALS.keys()[0],
                           password=CREDENTIALS[CREDENTIALS.keys()[0]],
                           project_name='admin',
                           user_domain_id='default',
                           project_domain_id='default')
        self.sess = k_session.Session(auth=auth)
        self.cinder = cinder_client.Client(session=self.sess)

    def volumelist(self):
        vol_list = self.cinder.volumes.list()
        return vol_list

class DeployOpenStackCloud():

    def deploy(self,ip):
            os.system("cd /home/ubuntu/OpenStack-Hackathon-OSIC/static; ./first.sh %s" % ip)
          #  os.system('./first.sh')
