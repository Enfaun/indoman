from docker.errors import DockerException
from socketio import Namespace

from indoman.utils import docker, logging, format_error

class Containers(Namespace):
    def on_connect(self, sid, environ):
        pass

    def on_disconnect(self, sid):
        pass

    def on_list(self, sid, list_params={}):
        try:
            containers = docker.client.containers.list(**list_params)
            return [c.attrs for c in containers]
        except DockerException as ex:
            return format_error(ex)

    def on_run(self, sid, image, _command=None):
        try:
            container = docker.client.containers.run(image, command=_command, detach=True)
            return container.attrs
        except DockerException as ex:
            return format_error(ex)

    def on_logs(self, sid, container_id, log_params={}):

        try:
            container = docker.client.containers.get(container_id)
            return container.logs(**log_params)
        except DockerException as ex:
            return format_error(ex)

    def on_listen_logs(self, sid, container_id, log_params={}):
        try:
            container = docker.client.containers.get(container_id)
            self.enter_room(sid, container.id)
            self.emit("logs", container.logs(**log_params))
        except DockerException as ex:
            return format_error(ex)
