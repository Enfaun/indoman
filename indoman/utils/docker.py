from docker import DockerClient
def init(*args, **kwargs):
    global client
    client = DockerClient(*args, **kwargs)
