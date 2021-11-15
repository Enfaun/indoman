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

    def on_load(self, sid, data):
        try:
            images = docker.client.images.load(data)
            return [image.attrs for image in images]
        except DockerException as ex:
            return format_error(ex)

    def on_remove(self, sid, name, force=False, noprune=True):
        try:
            image = docker.client.images.remove(image=name, force=force, noprune=noprune)
        except DockerException as ex:
            return format_error(ex)

    def on_search(self, sid, term, limit=50):
        try:
            return docker.client.images.search(term=term, limit=limit)
        except DockerException as ex:
            return format_error(ex)

    def on_list(self, sid, repository=None, all=False, filters=None):
        try:
            image = docker.client.images.list(repository, all, filters)
            return [c.attrs for c in image]
        except DockerException as ex:
            return format_error(ex)
