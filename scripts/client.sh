dir='out'
interval=1
number=5
ip="192.168.100.7"
start_sock=10000
server=""

for ((i=start_sock;i<start_sock+number;i++))
do
    server="$server $i"
done

state="python ../src/client.py -o $dir -a $ip -i $interval -p $server -c -r"

echo "Executing ${state}"
eval $state