from docker.errors import DockerException
from socketio import Namespace

from indoman.utils import docker, logging, format_error

class Networks(Namespace):
    def on_list(self, sid, list_params={}):
        try:
            networks = docker.client.networks.list(**list_params)
            return [c.attrs for c in networks]
        except DockerException as ex:
            return format_error(ex)
