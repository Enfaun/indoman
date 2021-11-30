from docker.errors import DockerException
from docker.models.containers import Container
from socketio import Namespace

from indoman.utils import docker, logging, format_error, messages

class Containers(Namespace):
    def on_connect(self, sid, environ):
        pass

    def on_disconnect(self, sid):
        pass

    def on_list(self, sid, list_params={}):
        try:
            containers: Container = docker.client.containers.list(**list_params)
            return [c.attrs for c in containers]
        except DockerException as ex:
            return format_error(ex)

    def on_list_stats(self, sid):
        try:
            containers: Container = docker.client.containers.list(all=True)
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

    def on_remove(self, sid, container_id, remove_params={}):
        try:
            container: Container = docker.client.containers.get(container_id)
            container.remove(**remove_params)
        except DockerException as ex:
            return format_error(ex)

    def on_logs(self, sid, container_id, log_params={}):

        try:
            container: Container = docker.client.containers.get(container_id)
            return container.logs(**log_params)
        except DockerException as ex:
            return format_error(ex)

    def on_stop_listen_logs(self, sid, container_id):
        try:
            container: Container  = docker.client.containers.get(container_id)
            room = f"{sid}-{container.id}-log"
            if room in self.rooms(sid):
                self.leave_room(sid, room)
        except DockerException as ex:
            return format_error(ex)

    def on_listen_logs(self, sid, container_id, log_params={}):
        try:
            container: Container  = docker.client.containers.get(container_id)
            room = f"{sid}-{container.id}-log"
            self.enter_room(sid, room)
            stream = container.logs(stream=True, follow=True, **log_params)
            line = ""
            try:
                while True:
                    char = next(stream).decode("utf-8")
                    line += char
                    if char == "\n":
                        self.emit("logs", line, room)
                        line = ""
                    if room not in self.rooms(sid):
                        break
            except StopIteration:
                self.emit("logs", line, room)
                self.leave_room(sid, room)
        except DockerException as ex:
            return format_error(ex)
