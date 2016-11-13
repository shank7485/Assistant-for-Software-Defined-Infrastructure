sudo sed -i '1s/^/nameserver 8.8.8.8 /' /etc/resolv.conf
sudo apt-get -y install git
git clone https://github.com/openstack/openstack-ansible.git
cd openstack-ansible
sudo scripts/bootstrap-ansible.sh
sudo scripts/bootstrap-aio.sh
sudo openstack-ansible playbooks/setup-everything.yml
