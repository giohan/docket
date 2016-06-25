# Dockable #

**Dockable** is a command line utility that helps you build docker images, deploy containers and monitor running instances. It uses Docker's [Remote API](https://docs.docker.com/engine/reference/api/docker_remote_api/) in order to run it from any machine without having to install docker.

## Features ##

- Builds image based on application and Dockerfile placed under certain directory
- Creates containers from this image
- Helps you monitor container health
- Logs from all containers are placed in the */container-logs* directory of the host machine

## Get Started ##

#### Prerequisites ####

The only thing you need to have installed in order to start using dockable is *python* and *pip*. The script takes care of installing any other needed libraries

To get started, you have to clone the repository to your computer.
~~~
git clone https://hantzo@bitbucket.org/hantzo/dockable.git /your/target/dir
export PATH=$PATH:/your/target/dir/dockable
~~~

## Usage ##

- Basic commands:
~~~
usage: dockable {build,containers,list,monitor} [-h] ...

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
usage: dockable build [-h] [-u URL] [-n NUM_INSTANCES] [-i IMAGE_NAME]
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
~~~
- Monitor:
~~~
usage: dockable monitor [-h] [-u URL] [--auto-update]

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
usage: dockable containers [-h] [-u URL] --id ID {start,stop,rm}

Helps you start|stop|rm containers by ID

positional arguments:
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
dockable build --url http://<ip>:<port> -i test/image -n 3
~~~
- Get metrics of all running containers
~~~
dockable monitor --url http://<ip>:<port>
~~~
- Stop and remove a running container
~~~
dockable containers stop --id <container id or name> --url http://<ip>:<port>
dockable containers rm --id <container id or name> --url http://<ip>:<port>
~~~
- Get list of all containers, including not running
~~~
dockable list --url http://<ip>:<port> --all
~~~

## Project Structure ##
~~~~
├── application  
│   ├── Dockerfile  
│   ├── package.json  
│   └── server.js  
├── config  
│   └── container.spec  
├── dockable  
├── lib  
│   ├── containers.py  
│   ├── docker.py  
│   ├── __init__.py  
│   └── monitoring.py  
└── README.md  
~~~~

- Anything placed under the *application/* directory is used to build the image.
- container.spec is used to create containers.