from novaclient import client

VERSION = '2'
USERNAME = 'admin'
PASSWORD = '1'
PROJECT_ID = 'cd1e4f37af1e4b58bcf8c4b6c18c3c5a'
AUTH_URL = 'http://172.99.106.120:5000/'


nova = client.Client(VERSION, USERNAME, PASSWORD, PROJECT_ID, AUTH_URL)
print(nova.flavors.list())

#
# from subprocess import call
#
# call(["ls", "-l"])
