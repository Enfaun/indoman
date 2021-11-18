import logging
from json import load as json_load, loads as json_loads, dumps as json_dumps, JSONDecodeError
from os import mkdir, removedirs
from os.path import isdir, join as path_join, isfile
from shutil import rmtree
from zipfile import ZipFile

from docker.models.containers import Container
from docker.models.networks import Network
from indoman.utils import errors, constants, docker, logging


def load_check_recipe(recipe_path, variables, environment_variables):
    recipefp = open(recipe_path)
    recipe = json_load(recipefp)
    recipefp.close()
    # checks for variable
    for variable in recipe["variables"]:
        if variable.get("required") == True:  # has to be this redundant because if it's string don't accept it
            if not variable["key"] in variables:
                raise errors.MISSING_VARIABLE
    # checks for environment variable
    for container in recipe["containers"]:
        if "environment_variables" in container:
            for env in container["environment_variables"]:
                if env.get("required") == True:  # same as above
                    if not env["key"] in environment_variables[container["name"]]:
                        raise errors.MISSING_VARIABLE
    return recipe


def replace_variables(recipe, variables, result_prefix_dir):
    recipe_str = json_dumps(recipe)
    logging.logger.debug(recipe)
    logging.logger.debug(recipe_str)
    for key, value in variables.items():
        logging.logger.debug(f"Replacing %{key}% to {value}")
        recipe_str = recipe_str.replace(f"%{key}%", str(value))
        logging.logger.debug(recipe_str)
    recipe_str = recipe_str.replace("%CRAFTED_PREFIX_DIR%", result_prefix_dir)
    recipe = json_loads(recipe_str)
    return recipe


def prepare_artifact_directory(recipe_name, prefix):
    result_prefix_dir = path_join(constants.CRAFTED_PREFIX_DIR, f"{prefix}_{recipe_name}")
    if not isdir(constants.CRAFTED_PREFIX_DIR):
        mkdir(constants.CRAFTED_PREFIX_DIR)
    if isdir(result_prefix_dir):
        raise FileExistsError
    mkdir(result_prefix_dir)
    return result_prefix_dir


def fail_cleanup(network, containers, directory):
    if network:
        network.remove()
    for container in containers:
        container.remove()
    rmtree(directory)



def create_network(recipe_name, prefix) -> Network:
    network_name = f"{prefix}_{recipe_name}"
    network = docker.client.networks.create(network_name)
    return network


def create_container(container_recipe, main_recipe_name, prefix, variables, environment_variables) -> Container:
    container_name = f"{prefix}_{main_recipe_name}_{container_recipe['name']}"
    image_name = container_recipe["from"]
    kwargs = {}
    ports = container_recipe.get("ports")
    if ports:
        port_args = {}
        for container_port, host in ports.items():
            host_interface, host_port = host.split(":")
            port_args.update({container_port: (host_interface, host_port, )})
        kwargs.update({"ports": port_args})
    container = docker.client.containers.create(image_name,
                                                name=container_name,
                                                detach=True,
                                                environment=environment_variables, **kwargs)
    return container
