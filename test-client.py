import pdb
from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient import client
from neutronclient.v2_0 import client as neutron_client


def createJSONResponse(*argv):
    try:
       argv[3]
    except Exception:
       button = False
    else:
       button = True
    response = "{\"message\": \""+argv[2]+"\",\"type\": \""+argv[0]+"\""
    l = []
    if argv[1] is not None:
         response = response + ",\"list\":["
         for a in argv[1]:
                temp = str(a).split(":")[1].strip()[:-1]
                temp1 = "{\"value\": \""+temp+"\"},"
                response = response + temp1
         response = response[:-1] + "]"
    response = response + ",\"button\":\""+str(button)+"\""
    response = response+ "}"
    return response


auth = v3.Password(auth_url='http://192.168.0.12:5000/v3',
                   username='admin',
                   password='1',
                   project_name='admin',
                   user_domain_id='default',
                   project_domain_id='default')
sess = session.Session(auth=auth)
nova = client.Client("2.1", session=sess)
#nova.servers.create("nish",flavor="m1.tiny")
neutron = neutron_client.Client(session=sess)
#response = createJSONResponse("AZ",nova.availability_zones.list(),"msg")
#print(response)
list = nova.servers.list()

network_list = neutron.list_networks()
netlist = []
temp_list = network_list['networks']
for i in temp_list:
    for k, v in i.iteritems():
         if str(k)=='name':
             k1 = '<'+str(k)
             v1 = str(v)+'>'
             w = k1+':'+v1
             netlist.append(w)
print netlist
print nova.availability_zones.list()
print createJSONResponse("",None,"Plain message")
