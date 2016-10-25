import pdb
from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient import client
auth = v3.Password(auth_url='http://192.168.0.179:5000/v3',
                   username='admin',
                   password='secret',
                   project_name='admin',
                   user_domain_id='default',
                   project_domain_id='default')
sess = session.Session(auth=auth)
nova = client.Client("2.1", session=sess)
print(nova.flavors.list())
print(nova.servers.list())
