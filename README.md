# Docket #

**Docket** is a command line utility that helps you build docker images, deploy containers and monitor running instances. It uses Docker's [Remote API](https://docs.docker.com/engine/reference/api/docker_remote_api/) in order to run it from any machine without having to install docker.

## Features ##

- Builds image based on application and Dockerfile placed under certain directory
- Creates containers from this image
- Helps you monitor container health
- Logs from all containers are placed in the */container-logs* directory of the host machine
- Tested on: OSX 10.10, CentOS 7, Ubuntu 14.04 and 16.04

## Project Structure ##
~~~~
├── application  
│   ├── Dockerfile  
│   ├── package.json  
│   └── server.js  
├── config  
│   └── container.spec  
├── docket
├── lib  
│   ├── containers.py  
│   ├── docker.py  
│   ├── __init__.py  
│   └── monitoring.py  
└── README.md  
~~~~

- The *application/* directory is the default directory where the Dockerfile and all application files are placed.
- *container.spec* is used by default to create containers.

## Get Started ##

#### Prerequisites ####

The only thing you need to have installed in order to start using docket is *python* and *pip*. The script takes care of installing any other needed libraries.

To get started, you have to clone the repository to your computer.
~~~
$ git clone https://github.com/giohan/docket.git
$ cd docket
$ export PATH=$PATH:`pwd`
$ chmod +x docket
~~~
~~~
$ docket build --url http://<docker-host>:<port> -n <number of instances>
~~~
**Note:** If you want to build the image without creating containers, just run with ```-n 0```.
If you do so, later you can create containers without building the image again:
~~~
docket build --url http://<docker-host>:<port> -n 3 --container-only
~~~

When running on ubuntu server 16.04, sometimes an import error appeared. This was due to pip locale settings. To get past this do:
~~~
$ export LC_ALL=C
~~~
## Usage ##

- Basic commands:
~~~
usage: docket {build,containers,list,monitor} [-h] ...

subcommands:
  {build,containers,list,monitor}
    build               Builds image and creates containers
    containers          Container operations
    list                Returns a list of running containers
    monitor             Monitor running containers

optional arguments:
  -h, --help            show this help message and exit
~~~

- Build:
~~~
usage: docket build [-h] [-u URL] [-n NUM_INSTANCES] [-i IMAGE_NAME]
                      [-d DIRECTORY] [-c CONTAINER_SPEC]

Build a docker image from given app and create a number of containers

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     The url where the docker daemon is running. Format:
                        "http://<ip>:<port>"
  -n NUM_INSTANCES, --num-instances NUM_INSTANCES 
                        Number of container instances to create after building
                        the image. Default=1
  -i IMAGE_NAME, --image-name IMAGE_NAME
                        Name of the created image
  -d DIRECTORY, --directory DIRECTORY
                        Directory of the application files. Path can be
                        absolute or relative and must contain Dockerfile.
  -c CONTAINER_SPEC, --container-spec CONTAINER_SPEC
                        JSON file containing parameters for creating the
                        containers. Must be carefull with "Binds" in order to
                        maintain centralized logging
  --container-only      Use this if you want to create containers from
                        existing image
~~~
- Monitor:
~~~
usage: docket monitor [-h] [-u URL] [--auto-update]

Creates a table with basic metrics for each container

optional arguments:
  -h, --help         show this help message and exit
  -u URL, --url URL  The url where the docker daemon is running. Format:
                     "http://<ip>:<port>"
  --auto-update      Makes the metrics table auto-update in a "top"-like
                     manner
~~~
- Container Operations:
~~~
usage: docket containers [-h] [-u URL] --id ID {start,stop,rm}

Helps you start|stop|rm containers by ID

subcommands:
  {start,stop,rm}    The action to do on the specified container. For "rm" the
                     container needs to be stopped first.

optional arguments:
  -h, --help         show this help message and exit
  -u URL, --url URL  The url where the docker daemon is running. Format:
                     "http://<ip>:<port>"
  --id ID            REQUIRED  Id of the container you want to effect
~~~

### Examples ###

- Build an image called test/image and create 3 instances from this image.
~~~
docket build --url http://<ip>:<port> -i test/image -n 3
~~~
- Get metrics of all running containers
~~~
docket monitor --url http://<ip>:<port>
~~~

- Stop and remove a running container
~~~
docket containers stop --id <container id or name> --url http://<ip>:<port>
docket containers rm --id <container id or name> --url http://<ip>:<port>
~~~
- Get list of all containers, including not running
~~~
docket list --url http://<ip>:<port> --all
~~~

#### Sample output: ####
~~~
$ docket monitor --url http://139.162.195.16:4243
+---------------------+---------+--------------------+-------------------+
|        Name         |  CPU %  | Mem Usage / Limit  |     Net I / O     |
+=====================+=========+====================+===================+
| kickass_lalande     |  0.0 %  | 73.18 MB / 12.6 GB | 648.0 B / 738.0 B |
+---------------------+---------+--------------------+-------------------+
| pedantic_tesla      |  0.0 %  | 73.19 MB / 12.6 GB | 1.39 KB / 648.0 B |
+---------------------+---------+--------------------+-------------------+
| furious_archimedes  |  0.0 %  | 73.18 MB / 12.6 GB | 4.51 KB / 738.0 B |
+---------------------+---------+--------------------+-------------------+
| sharp_chandrasekhar |  0.0 %  | 73.18 MB / 12.6 GB | 5.86 KB / 738.0 B |
+---------------------+---------+--------------------+-------------------+
| prickly_payne       |  0.0 %  | 73.18 MB / 12.6 GB | 6.37 KB / 738.0 B |
+---------------------+---------+--------------------+-------------------+
~~~
~~~
$ docket build --url http://139.162.195.16:4243 -i test/image
Building image "test/image" from directory "application/"... 
	(This might take a while)
Image built successfully!
Creating "1" containers from image "test/image"... 
Created 1 containers!
started container d273f373aab8dd470cd82fb8304b153fe31dbd2aa01eac141dc57adb443cd454
+---------------+---------+------------+-------------+------------+
|     Name      | Status  |     IP     |    Ports    |   Image    |
+===============+=========+============+=============+============+
| nauseous_bell | running | 172.17.0.5 | 8080: 32871 | test/image |
|               |         |            | 22: 32872   |            |
+---------------+---------+------------+-------------+------------+
~~~
~~~
$ docket list --url http://139.162.195.16:4243 --all
+---------------------+---------+-------------+-------------+------------+
|        Name         | Status  |     IP      |    Ports    |   Image    |
+=====================+=========+=============+=============+============+
| sharp_wing          | running | 172.17.0.13 | 8080: 32885 | test/image |
|                     |         |             | 22: 32886   |            |
+---------------------+---------+-------------+-------------+------------+
| nauseous_bell       | running | 172.17.0.5  | 8080: 32871 | test/image |
|                     |         |             | 22: 32872   |            |
+---------------------+---------+-------------+-------------+------------+
| kickass_lalande     | running | 172.17.0.6  | 8080: 32869 | test/image |
|                     |         |             | 22: 32870   |            |
+---------------------+---------+-------------+-------------+------------+
| pedantic_tesla      | running | 172.17.0.4  | 8080: 32867 | test/image |
|                     |         |             | 22: 32868   |            |
+---------------------+---------+-------------+-------------+------------+
| sad_noyce           | exited  |             |             | test/image |
+---------------------+---------+-------------+-------------+------------+
| furious_archimedes  | exited  |             |             | test/image |
+---------------------+---------+-------------+-------------+------------+
| sharp_chandrasekhar | running | 172.17.0.3  | 8080: 32855 | test/image |
|                     |         |             | 22: 32856   |            |
+---------------------+---------+-------------+-------------+------------+
| prickly_payne       | running | 172.17.0.2  | 8080: 32853 | test/image |
|                     |         |             | 22: 32854   |            |
+---------------------+---------+-------------+-------------+------------+
~~~