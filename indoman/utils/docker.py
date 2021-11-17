import eventlet
import docker
_docker = eventlet.import_patched("docker")

client: docker.DockerClient


def init(*args, **kwargs):
    global client
    client = _docker.DockerClient(*args, **kwargs)
