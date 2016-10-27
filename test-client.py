import pdb
from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient import client
from neutronclient.v2_0 import client as neutron_client


def createJSONResponse(type,list,msg):
    response = "{message: \""+msg+"\",\"list\":["
    l = []
    for a in list:
         temp = str(a).split(":")[1].strip()[:-1]
         temp1 = "{\"value\": \""+type+"\", \"onclick\": \"setvariable("+type+","+temp+")\"},"
         response = response + temp1
         #print temp1
    response = response[:-1] + "]}"
    return response

auth = v3.Password(auth_url='http://172.99.106.89:80/v3',
                   username='admin',
                   password='secret',
                   project_name='admin',
                   user_domain_id='default',
                   project_domain_id='default')
sess = session.Session(auth=auth)
nova = client.Client("2.1", session=sess)
#nova.servers.create("nish",flavor="m1.tiny")
neutron = neutron_client.Client(session=sess)
response = createJSONResponse("AZ",nova.availability_zones.list(),"msg")
print(response)
list = nova.servers.list()
print(neutron.list_networks())
