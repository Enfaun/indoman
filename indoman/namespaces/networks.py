from docker.errors import DockerException
from docker.models.containers import Container
from docker.models.networks import Network
from socketio import Namespace

from indoman.utils import docker, logging, format_error

class Networks(Namespace):
    def on_list(self, sid, list_params={}):
        try:
            networks = docker.client.networks.list(**list_params)
            return [c.attrs for c in networks]
        except DockerException as ex:
            return format_error(ex)

    def on_create(self, sid, name, create_params={}):
        try:
            docker.client.networks.create(name, **create_params)
        except DockerException as ex:
            return format_error(ex)

    def on_remove(self, sid, network_id):
        try:
            network: Network = docker.client.networks.get(network_id)
            network.remove()
        except DockerException as ex:
            return format_error(ex)

    def on_connect(self, sid, container_id, network_id, connect_params={}):
        try:
            network: Network = docker.client.networks.get(network_id)
            container: Container = docker.client.containers.get(container_id)
            network.connect(container, **connect_params)
        except DockerException as ex:
            return format_error(ex)

    def on_disonnect(self, sid, container_id, network_id):
        try:
            network: Network = docker.client.networks.get(network_id)
            container: Container = docker.client.containers.get(container_id)
            network.disconnect(container)
        except DockerException as ex:
            return format_error(ex)
