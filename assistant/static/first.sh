scp -o "StrictHostKeyChecking no" -i ~/deploy_key.pem second.sh ubuntu@$1:/home/ubuntu
ssh -o "StrictHostKeyChecking no" -i ~/deploy_key.pem ubuntu@$1 "./second.sh &> log_"$1".txt &"
