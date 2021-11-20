from docker.errors import DockerException
from socketio import Namespace

from indoman.utils import docker, logging, format_error, messages

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

    def on_list_stats(self, sid):
        try:
            containers = docker.client.containers.list(all=True)
            return {container.id: container.stats(stream=False) for container in containers}
        except DockerException as ex:
            return format_error(ex)

    def on_run(self, sid, image, _command=None):
        try:
            docker.client.containers.run(image, command=_command, detach=True)
            return messages.SUCCESS
        except DockerException as ex:
            return format_error(ex)

    def on_start(self, sid, container_id, start_params=None):
        try:
            docker.client.containers.get(container_id).start(**start_params)
            return messages.SUCCESS
        except DockerException as ex:
            return format_error(ex)

    def on_stop(self, sid, container_id, stop_params={}):
        try:
            docker.client.containers.get(container_id).stop(**stop_params)
        except DockerException as ex:
            return format_error(ex)

    def on_logs(self, sid, container_id, log_params={}):

        try:
            container = docker.client.containers.get(container_id)
            return container.logs(**log_params)
        except DockerException as ex:
            return format_error(ex)

    def on_stop_listen_logs(self, sid, container_id):
        try:
            container = docker.client.containers.get(container_id)
            room = f"{sid}-{container.id}-log"
            if room in self.rooms(sid):
                self.leave_room(sid, room)
        except DockerException as ex:
            return format_error(ex)

    def on_listen_logs(self, sid, container_id, log_params={}):
        try:
            container = docker.client.containers.get(container_id)
            room = f"{sid}-{container.id}-log"
            self.enter_room(sid, room)
            stream = container.logs(stream=True, follow=True, **log_params)
            try:
                while True:
                    line = next(stream).decode("utf-8")
                    self.emit("logs", line, room)
                    if room not in self.rooms(sid):
                        break
            except StopIteration:
                self.leave_room(sid, room)
        except DockerException as ex:
            return format_error(ex)
