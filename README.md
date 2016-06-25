# Dockable #

**Dockable** is a command line utility that helps you build docker images, deploy containers and monitor running instances. It uses Docker's [Remote API](https://docs.docker.com/engine/reference/api/docker_remote_api/) in order to run it from any machine without having to install docker.

## Features ##

- Builds image based on application and Dockerfile placed under certain directory
- Creates containers from this image
- Helps you monitor container health
- Logs from all containers are placed in the */container-logs* directory of the host machine

## Usage ##

**TODO**

### Examples ###

**TODO**

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
