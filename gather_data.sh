#!/bin/bash

port='31222'
ip='139.80.98.239'

repeat='60'
time_interval='100000000'

memory_file="/sys/fs/cgroup/memory/docker/972e3860906ba4392f9b28bfbe085eda6e58a68e8c995721bbd77c7ccc263978/memory.stat"
memory_file2="/sys/fs/cgroup/memory/docker/972e3860906ba4392f9b28bfbe085eda6e58a68e8c995721bbd77c7ccc263978/memory.usage_in_bytes"
memory_out_file="/tmp/memory_log.txt"

cpu_file="/sys/fs/cgroup/cpuacct/docker/972e3860906ba4392f9b28bfbe085eda6e58a68e8c995721bbd77c7ccc263978/cpuacct.usage"
cpu_out_file="/tmp/cpu_log.txt"

block_file="/sys/fs/cgroup/blkio/docker/972e3860906ba4392f9b28bfbe085eda6e58a68e8c995721bbd77c7ccc263978/blkio.throttle.io_service_bytes"
block_out_file="/tmp/block_log.txt"

#pid=`docker inspect -f '{{ .State.Pid }}' 972e3860906ba4392f9b28bfbe085eda6e58a68e8c995721bbd77c7ccc263978`
network_file="/proc/2601/net/dev"
network_out_file="/tmp/network_log.txt"

file_c_vm='cpu_log.txt'
file_m_vm='memory_log.txt'
file_b_vm='block_log.txt'
file_n_vm='network_log.txt'

#Add more variables of the locations of CPU, block I/O and Network files.
#Call gather_data executable inside the VM to gather data and write to /tmp folder.
#Once the files are transfered back to host, call a python program to process the data and write(append) the duration and other information into another file.

nc -l $port | tar -x & pid5=$!

#echo "/tmp/exec/gather_data $memory_file $memory_file2 $memory_out_file $repeat $time_interval & /tmp/exec/gather_data $cpu_file $cpu_out_file $repeat $time_interval &/tmp/exec/gather_data $bl\
#ock_file $block_out_file $repeat $time_interval & /tmp/exec/gather_data $network_file $network_out_file $repeat $time_interval "> ~/Library/Containers/com.docker.docker/Data/vms/0/tty;


#wait till all gathering commands finished and send all files.
echo "/tmp/exec/gather_data $memory_file $memory_file2 $memory_out_file $repeat $time_interval &
pid1=$! ; /tmp/exec/gather_data $cpu_file $cpu_out_file $repeat $time_interval & pid2=$! ; /tmp/exec/gather_data $block_file $block_out_file $repeat $time_interval & pid3=$! ; /tmp/exec/gather_data $network_file $network_out_file $repeat $time_interval & pid4=$!  wait $pid1 && wait $pid2 && wait $pid3 && wait $pid4 && tar -C /tmp -c $file_c_vm $file_m_vm $file_n_vm $file_b_vm | nc $ip $port && rm /tmp/memory_log.txt && rm /tmp/network_log.txt && rm /tmp/cpu_log.txt && rm /tmp/block_log.txt "> ~/Library/Containers/com.docker.docker/Data/vms/0/tty ;

wait $pid5 && python3 process_overhead.py memory_60times_100ms.txt cpu_60times_100ms.txt block_60times_100ms.txt network_60times_100ms.txt

#while [ ! -f /Users/james/Documents/cosc490/log/terminate.txt ]
#do true
#done;
#kill pid5
#echo "(/tmp/exec/gather_data_overhead $memory_file $memory_out_file 100000 & /tmp/exec/gather_data_overhead $cpu_file $cpu_out_file 100000 &/tmp/exec/gather_data_overhead $block_file $block_out_file 100000 & /tmp/exec/gather_data_overhead $network_file $network_out_file 100000 ) && tar -C /tmp -c $file_c_vm $file_m_vm $file_n_vm $file_b_vm | nc $ip $port "> ~/Library/Containers/com.docker.docker/Data/vms/0/tty;
