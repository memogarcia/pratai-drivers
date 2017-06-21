# Docker driver

## Configure docker

enable docker deamon to be accessible by tcp://127.0.0.1

add this to '/etc/default/docker'

    DOCKER_OPTS='-H tcp://127.0.0.1:4243 -H unix:///var/run/docker.sock'

    sudo service docker restart

## Run a container

flask web server should run on the host where docker is deployed


if the name of the images contains /, needs to be replaced by --- in the request

    http://178.62.199.180:9999/pull/memogarcia---python27


**Deprecated**
when a new container gets executed it exposes a random port to be accessed to.

from python can be retrieved like this:

    resp["NetworkSettings"]["Ports"]["5000/tcp"][0]["HostPort"]


the response should be the output of **docker inspect**
**End Deprecated**


## build a container

when an image is build the docker file gets created dynamically according to the user input

a `Dockerfile` is created in `/tmp/uuid/Dockerfile` from which docker builds the image.

a post request should be made with the following payload

    {
        "memory": 128,
        "tags": ["python27"],
        "runtime": "python27",
        "zip_location": "https://s3-eu-west-1.amazonaws.com/pratai/python27.zip",
        "name": "pratai_test"
    }


## TODO

  * how to execute long processes in python