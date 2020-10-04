# COSC490

A research project on the performance comparison between different CMS.
A fine-grained resource measurement tool is developed for containerized software.
This repository contains the source codes of the tool and the corresponding codes of workloads and graphs generator.
The defined workloads in this project are creating, updating, viewing, and deleting a post on a website based on WordPress and Drupal.

## All graphs generated from the experiments
Five runs of creating and viewing a post of a Drupal website and a WordPress website.

One zip file contains all the graphs from one run, for example, **drupal_create_post_run_1** contains all the graphs generated for the Drupal container and its database container, 32 graphs for one container. It has 64 graphs and 8 raw data files in total. 

## Needed files to run the tool.

    start.sh
    
    gather_resource_data
    
    process_data.py
    
    docker-compose_drupal
    
    docker-compose_wordpress

## Start the Drupal and WordPress containers.
- Download a chrome driver.

- Run the Docker Desktop.

- Change the name of the docker file to run Drupal and WordPress container, from docker-compose_drupal to docker-compose when running a Drupal website. The same thing applies to the WordPress website.

- Example: `docker-compose up -d`

## Pre-setup:
- If it is on Windows, need to install WSL and set up WSL following this guide https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly
, Then change in start.sh on line 9 about the IP address.

- Need to know the container's name that you wish to monitor, for example, wordpress_wordpress_1.

- Need to access the VM that manages Docker containers; run: `docker run -it --rm --privileged --pid=host justincormack/nsenter1`

- Use docker ps to get the name of the running container, put this name into variable name **'control_container_name'**

- Need to set up an **'exec'** folder which can execute the C program.

Run:
			
    cd /tmp    
    mkdir etc
    cd etc
    cp -ar /etc/* .
    cd ..  
    mount --bind /tmp/etc /etc        
    echo 'tmpfs /tmp/exec tmpfs defaults 0 0' >> /etc/fstab        
    mkdir exec       
    mount /tmp/exec

- Need to transfer the C program inside the VM, for example:

    On the host: `nc -l 50000  < gather_resource_data`
    On the VM: `nc 192.168.178.51 50000 > gather_resource_data`

## Running the tool:

On the host machine, in the folder which contains a chrome driver and the Python script 

    ./start.sh [operation] [container name] [container name]
    
    ./start.sh [operation] [container name]
    
    Operation: create, update, view, delete
    
    ./start.sh create wordpress_wordpress_1
    
    ./start.sh create wordpress_wordpress_1 wordpress_db_1
    
    ./start.sh create drupal_drupal_1
    
    ./start.sh create drupal_drupal_1 drupal_mysql_1

The default setting in start.sh is repeating: 2000 times, time interval: 10000000 (10ms)

This means the tool gathers data every 10ms for about 20s.

Change the values of the variable 'repeat' and 'time_interval' as needed. 
