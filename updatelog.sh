while true
do
  sleep 10s
  now=$(date +"%T");printf "\nI am getting updated "+$now >> static/log1.txt
done
