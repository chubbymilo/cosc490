#cosc490
Pre-setup:
If it is on Windows, need to install WSL and set up WSL following this guide https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly
Then change in start.sh on line 9 about the IP address.

1.Need to know the container's name that you wish to monitor, for example, wordpress_wordpress_1.
2.Need to access the VM that manages docker containers; run: docker run -it --rm --privileged --pid=host justincormack/nsenter1
Use docker ps to get the name of the running container, put this name into variable name 'control_container_name'
3.Need to set up a 'exec' folder which can execute C program; run:
cd /tmp
mkdir etc 
cd etc
cp -ar /etc/* .
cd ..
echo 'tmpfs /tmp/exec tmpfs defaults 0 0' >> /etc/fstab
mkdir exec
mount /tmp/exec

4.Need to transfer the C program inside the VM, for example:
On host: nc -l 50000  < gather_resource_data
On VM: nc 192.168.178.51 50000 > gather_resource_data

Running the tool:
On host machine, in the folder which contains a chrome driver and the Python script 
./start.sh [operation] [container name] [container name]
./start.sh [operation] [container name]
Operation: create, update, view, delete
./start.sh create wordpress_wordpress_1
./start.sh create wordpress_wordpress_1 wordpress_db_1
./start.sh create drupal_drupal_1
./start.sh create drupal_drupal_1 drupal_mysql_1

The default setting in start.sh is repeat: 2000, time interval : 10000000 (10ms)
This means the tool gathers data every 10ms for about 20s.
Change the variables values of repeat and time_interval as needed. 
