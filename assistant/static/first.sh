scp -i /home/ubuntu/OpenStack-Hackathon-OSIC/hack_key.pem /home/ubuntu/OpenStack-Hackathon-OSIC/static/second.sh ubuntu@$1:/home/ubuntu
ssh -i /home/ubuntu/OpenStack-Hackathon-OSIC/hack_key.pem  ubuntu@$1 "./second.sh &> log_"$1".txt &"
#scp -i /home/ubuntu/nish_key-2.pem  ubuntu@192.168.0.225:/home/ubuntu/log_192.168.0.225.txt .
