file='tmp.mp4'
interval=1
number=5
start_sock=10000
server=""

for ((i=start_sock;i<start_sock+number;i++))
do
    server="$server $i"
done

state="python ../src/server.py -f $file -n $number -i $interval -p $server -c"

echo "Executing ${state}"
eval $state