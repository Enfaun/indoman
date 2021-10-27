import eventlet
docker  = eventlet.import_patched("docker")
def init(*args, **kwargs):
    global client
    client = docker.DockerClient(*args, **kwargs)
