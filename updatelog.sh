while true
do
  sleep 10s
  now=$(date +"%T");printf "\nI am getting updated "+$now >> static/log_1.1.1.1.txt
done
