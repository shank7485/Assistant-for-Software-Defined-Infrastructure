git clone https://github.com/openstack/openstack-ansible.git
cd openstack-ansible
sudo scripts/bootstrap-ansible.sh > /home/ubuntu/zzz.txt
sudo scripts/bootstrap-aio.sh > /home/ubuntu/zzz.txt
sudo openstack-ansible playbooks/setup-everything.yml > /home/ubuntu/zzz.txt
