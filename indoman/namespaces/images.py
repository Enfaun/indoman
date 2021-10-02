from docker.errors import DockerException
from socketio import Namespace

from indoman.utils import docker, logging, format_error

class Images(Namespace):
    def on_pull(self, sid, repository, tag=None):
        try:
            image = docker.client.images.pull(repository, tag)
            return image.attrs
        except DockerException as ex:
            return format_error(ex)

    def on_get(self, sid, name):
        try:
            image = docker.client.images.get(name)
            return image.attrs
        except DockerException as ex:
            return format_error(ex)

    def on_list(self, sid, repository=None, all=False, filters=None):
        try:
            image = docker.client.images.list(repository, all, filters)
            return [c.attrs for c in image]
        except DockerException as ex:
            return format_error(ex)
