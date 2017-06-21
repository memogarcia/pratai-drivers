import subprocess
import os

from docker import Client

from utils import build_args


cli = Client(base_url='unix:///var/run/docker.sock', tls=False, version='1.18')


def create_subprocess(cmd):
    """
    Create a new subprocess in the OS
    :param cmd: command to execute in the subprocess
    :return: the output and errors of the subprocess
    """
    process = subprocess.Popen(cmd,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               env=os.environ, shell=True)
    return process.communicate()


def docker_run(cmd):
    """
    r = envoy.run(command)
    if r.std_err:
        return r.std_err
    return r.std_out
    """
    return create_subprocess(cmd)


def find_executable():
    cmd = "which docker"
    out, err = docker_run(cmd)
    return out


def run(image_id, payload, function_id, request_id):
    docker_exec = find_executable()
    cmd = "{} run -e function_id='{}' -e request_id='{}' -e pratai_payload='{}' -d {}"\
        .format(docker_exec, function_id, request_id, payload, image_id)
    out, err = docker_run(cmd)
    if err != '':
        pass
    else:
        pass
    return out


def build(json_payload):
    args = build_args(json_payload)
    docker_exec = find_executable()
    cmd = '{} {}'.format(docker_exec, args)
    out, err = docker_run(cmd)
    return out


def kill(container_id):
    docker_exec = find_executable()
    cmd = "{} kill {}".format(docker_exec, container_id)
    return docker_run(cmd)


def delete(image_id):
    docker_exec = find_executable()
    cmd = '{} rmi -f {}'.format(docker_exec, image_id)
    return docker_run(cmd)
