#!/bin/bash

if [ "$#" -eq 2 ]; then
    port='49999'
    #uncommon the line if the host OS is MAC.
    export ip=`ipconfig getifaddr en0`
    #uncommon the line if the host OS is windows.
    #export ip=`hostname -I | awk '{print $1}'`
    repeat='15000'
    time_interval='1000000'
    file_c_vm='cpu_log.txt'
    file_m_vm='memory_log.txt'
    file_b_vm='block_log.txt'
    file_n_vm='network_log.txt'

export container_id=$(docker inspect --format="{{.Id}}" $2)
export container_pid=`docker inspect -f '{{ .State.Pid }}' $container_id`

file_c_vm="${2}_${1}_${file_c_vm}"
file_m_vm="${2}_${1}_${file_m_vm}"
file_b_vm="${2}_${1}_${file_b_vm}"
file_n_vm="${2}_${1}_${file_n_vm}"

cpu_out_file="/tmp/${file_c_vm}"
memory_out_file="/tmp/${file_m_vm}"
block_out_file="/tmp/${file_b_vm}"
network_out_file="/tmp/${file_n_vm}"

cpu_file="/sys/fs/cgroup/cpuacct/docker/$container_id/cpuacct.usage"
memory_file="/sys/fs/cgroup/memory/docker/$container_id/memory.stat"
memory_file2="/sys/fs/cgroup/memory/docker/$container_id/memory.usage_in_bytes"
block_file="/sys/fs/cgroup/blkio/docker/$container_id/blkio.throttle.io_service_bytes"
network_file="/proc/$container_pid/net/dev"

va1=$(docker exec vigorous_buck /bin/sh -c "grep -n 'eth0:' $network_file")
target_index=${va1:0:1}

nc -l $port | tar -x &
export pid5=$!

#docker exec vigorous_buck /bin/sh -c "/tmp/exec/test_gather_data5 $network_file $network_out_file $target_index $repeat $time_interval && tar -C /tmp -c $file_n_vm | nc $ip $port "
#docker exec vigorous_buck /bin/sh -c " /tmp/exec/test_gather_data5 $cpu_file $cpu_out_file $repeat $time_interval && tar -C /tmp -c $file_n_vm | nc $ip $port "

#docker exec vigorous_buck /bin/sh -c " /tmp/exec/test_gather_data5 $memory_file $memory_file2 $memory_out_file $repeat $time_interval && tar -C /tmp -c $file_m_vm | nc $ip $port "
#docker exec vigorous_buck /bin/sh -c "/tmp/exec/test_gather_data5 $block_file $block_out_file $repeat $time_interval && tar -C /tmp -c $file_b_vm | nc $ip $port "



# docker exec vigorous_buck /bin/sh -c "/tmp/exec/test_gather_data5 $cpu_file $cpu_out_file $repeat $time_interval & export pid1=$! ;
# /tmp/exec/test_gather_data5 $memory_file $memory_file2 $memory_out_file $repeat $time_interval & export pid2=$! ;
# /tmp/exec/test_gather_data5 $block_file $block_out_file $repeat $time_interval & export pid3=$! ;
# /tmp/exec/test_gather_data5 $network_file $network_out_file $target_index $repeat $time_interval & export pid4=$! ;
# wait $pid1 && wait $pid2 && wait $pid3 && wait $pid4 &&
# rm $cpu_out_file ; rm $memory_out_file ; rm $block_out_file ; rm $network_out_file "


docker exec vigorous_buck /bin/sh -c "/tmp/exec/gather_resource_data $cpu_file $cpu_out_file $repeat $time_interval & export pid1=$! ;
/tmp/exec/gather_resource_data $memory_file $memory_file2 $memory_out_file $repeat $time_interval & export pid2=$! ;
/tmp/exec/gather_resource_data $block_file $block_out_file $repeat $time_interval & export pid3=$! ;
/tmp/exec/gather_resource_data $network_file $network_out_file $target_index $repeat $time_interval & export pid4=$! ;
wait $pid1 && wait $pid2 && wait $pid3 && wait $pid4 &&
tar -C /tmp -c $file_c_vm $file_m_vm $file_b_vm $file_n_vm | nc $ip $port &&
rm $cpu_out_file ; rm $memory_out_file ; rm $block_out_file ; rm $network_out_file " & python3 process_data.py $1 $2

#& python3 process_resource_data.py $1 $2
# & python3 process_data3.py $1 $2
 
elif [ "$#" -eq 3 ]; then
port='49999'
#ip='192.168.178.51'
#export ip=`ipconfig getifaddr en0`
export ip=`hostname -I | awk '{print $1}'`
repeat='15000'
time_interval='1000000'
file_c_vm='cpu_log.txt'
file_m_vm='memory_log.txt'
file_b_vm='block_log.txt'
file_n_vm='network_log.txt'

export container_id=$(docker inspect --format="{{.Id}}" $2)
export container_pid=`docker inspect -f '{{ .State.Pid }}' $container_id`

export container_id2=$(docker inspect --format="{{.Id}}" $3)
export container_pid2=`docker inspect -f '{{ .State.Pid }}' $container_id2`

file_c_vm1="${2}_${1}_${file_c_vm}"
file_m_vm1="${2}_${1}_${file_m_vm}"
file_b_vm1="${2}_${1}_${file_b_vm}"
file_n_vm1="${2}_${1}_${file_n_vm}"

file_c_vm2="${3}_${1}_${file_c_vm}"
file_m_vm2="${3}_${1}_${file_m_vm}"
file_b_vm2="${3}_${1}_${file_b_vm}"
file_n_vm2="${3}_${1}_${file_n_vm}"

cpu_out_file="/tmp/${file_c_vm1}"
memory_out_file="/tmp/${file_m_vm1}"
block_out_file="/tmp/${file_b_vm1}"
network_out_file="/tmp/${file_n_vm1}"

cpu_out_file2="/tmp/${file_c_vm2}"
memory_out_file2="/tmp/${file_m_vm2}"
block_out_file2="/tmp/${file_b_vm2}"
network_out_file2="/tmp/${file_n_vm2}"

cpu_file="/sys/fs/cgroup/cpuacct/docker/$container_id/cpuacct.usage"
memory_file="/sys/fs/cgroup/memory/docker/$container_id/memory.stat"
memory_file2="/sys/fs/cgroup/memory/docker/$container_id/memory.usage_in_bytes"
block_file="/sys/fs/cgroup/blkio/docker/$container_id/blkio.throttle.io_service_bytes"
network_file="/proc/$container_pid/net/dev"

cpu_file2="/sys/fs/cgroup/cpuacct/docker/$container_id2/cpuacct.usage"
memory_file3="/sys/fs/cgroup/memory/docker/$container_id2/memory.stat"
memory_file4="/sys/fs/cgroup/memory/docker/$container_id2/memory.usage_in_bytes"
block_file2="/sys/fs/cgroup/blkio/docker/$container_id2/blkio.throttle.io_service_bytes"
network_file2="/proc/$container_pid2/net/dev"


#find the index of eth0, as it changes over the time
va1=$(docker exec vigorous_buck /bin/sh -c "grep -n 'eth0:' $network_file")
target_index=${va1:0:1}

va1=$(docker exec vigorous_buck /bin/sh -c "grep -n 'eth0:' $network_file2")
target_index2=${va1:0:1} 


nc -l $port | tar -x &
export pid5=$!

docker exec vigorous_buck /bin/sh -c "/tmp/exec/gather_resource_data $cpu_file $cpu_out_file $repeat $time_interval & export pid1=$! ;
/tmp/exec/gather_resource_data $cpu_file2 $cpu_out_file2 $repeat $time_interval & export pid6=$! ;
/tmp/exec/gather_resource_data $memory_file $memory_file2 $memory_out_file $repeat $time_interval & export pid2=$! ;
/tmp/exec/gather_resource_data $memory_file3 $memory_file4 $memory_out_file2 $repeat $time_interval & export pid7=$! ;
/tmp/exec/gather_resource_data $block_file $block_out_file $repeat $time_interval & export pid3=$! ;
/tmp/exec/gather_resource_data $block_file2 $block_out_file2 $repeat $time_interval & export pid8=$! ;
/tmp/exec/gather_resource_data $network_file $network_out_file $target_index $repeat $time_interval & export pid4=$! ;
/tmp/exec/gather_resource_data $network_file2 $network_out_file2 $target_index2 $repeat $time_interval & export pid9=$! &&
wait $pid1 && wait $pid2 && wait $pid3 && wait $pid4 && wait $pid6 && wait $pid7 && wait $pid8 && wait $pid9 &&
tar -C /tmp -c $file_c_vm1 $file_m_vm1 $file_b_vm1 $file_n_vm1 $file_c_vm2 $file_m_vm2 $file_b_vm2 $file_n_vm2 | nc $ip $port &&
rm $cpu_out_file ; rm $memory_out_file ; rm $block_out_file ; rm $network_out_file ;
rm $cpu_out_file2 ; rm $memory_out_file2 ; rm $block_out_file2 ; rm $network_out_file2 " & python3 process_data.py $1 $2 $3 
#& python3 process_resource_data.py $1 $2 $3
#& python3 process_resource_data3.py $1 $2 $3
#& python3 process_data3.py $1 $2 $3 

else
   echo "Usage: [operation], [container_name]"
   echo "Usage: [operation], [container_name], [container_name]"
   echo "Example: ./example.sh update wordpress1, wordpress_db1"
fi