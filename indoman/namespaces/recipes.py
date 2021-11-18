from json import load as json_load, loads as json_loads, dumps as json_dumps, JSONDecodeError
from os import mkdir, listdir, removedirs
from os.path import isdir, join as path_join, isfile
from shutil import move
from traceback import format_exc
from zipfile import ZipFile, BadZipfile

from docker.errors import ImageNotFound
from socketio import Namespace

from indoman.recipes import import_recipe, get_recipe, list_recipes, remove_recipe
from indoman.recipes import craft_recipe
from indoman.utils import docker, logging, format_error, errors, constants, messages


class Recipes(Namespace):
    def on_connect(self, sid, environ):
        pass

    def on_disconnect(self, sid):
        pass

    def on_upload(self, sid, data):
        if not isdir(constants.RECIPES_DIR): mkdir(constants.RECIPES_DIR)
        logging.logger.info(f"{sid} uploading recipes...")
        zip_filename = path_join(constants.TEMP_DIR, f"recipe-tmp-{sid}.zip")
        file = open(zip_filename, "wb")
        file.write(data)
        file.close()
        room = zip_filename + "-room"
        self.enter_room(sid, room)
        try:
            self.send(messages.RECIPE_UNPACKING, room)
            tmp_dir = import_recipe.unpack_zip(zip_filename)
            self.send(messages.RECIPE_EXTRACT_FINISHED, room)
            import_recipe.parse_recipe(tmp_dir)
            self.send(messages.RECIPE_IMPORT_FINISHED, room)
        except BadZipfile:
            logging.logger.error(format_exc())
            self.send(errors.BAD_ZIPFILE, room)
        except Exception as e:
            logging.logger.error(format_exc())
            self.send(format_error(e))
        finally:
            self.leave_room(sid, room)

    def on_craft(self, sid, recipe_name, prefix, variables, environment_variables):
        room = f"{sid}=craft-{prefix}_{recipe_name}"
        self.enter_room(sid, room)
        recipe_path = path_join(constants.RECIPES_DIR, recipe_name, "recipe.json")
        network = None
        created_containers = []
        try:
            result_prefix_dir = craft_recipe.prepare_artifact_directory(recipe_name, prefix)
            self.send(messages.CRAFT_PREPARE, room)
            recipe = craft_recipe.load_check_recipe(recipe_path, variables, environment_variables)
            recipe = craft_recipe.replace_variables(recipe, variables, result_prefix_dir)
            network = craft_recipe.create_network(recipe_name, prefix)
            self.send(messages.CRAFT_NETWORK_CREATED, room)
            for container_recipe in recipe["containers"]:
                image = container_recipe["from"]
                try:
                    docker.client.images.get(image)
                except ImageNotFound:
                    message = messages.CRAFT_PULLING_IMAGE
                    message.update({"image": image})
                    self.send(message, room)
                    docker.client.images.pull(image)
                env = environment_variables[container_recipe["name"]]
                container = craft_recipe.create_container(container_recipe, recipe_name, prefix, variables, env)
                created_containers.append(container)
                default_alias = f"{prefix}_{recipe_name}_{container_recipe['name']}"
                alias = container_recipe.get("network_alias", default=default_alias)
                network.connect(container, [alias, ])
                message = messages.CRAFT_CONTAINER_CREATED
                message.update({"container": container.name})
                self.send(message, room)
            self.send(messages.SUCCESS, room)
        except JSONDecodeError:
            logging.logger.error(format_exc())
            self.send(format_error(errors.INCORRECT_RECIPE_JSON_FORMAT))
        except Exception as e:
            logging.logger.error(format_exc())
            self.send(format_error(e))
            craft_recipe.fail_cleanup(network, created_containers, recipe_path)
        finally:
            self.leave_room(sid, room)

    def on_get_recipe(self, sid, name):
        return get_recipe(name)

    def on_list(self, sid, glob="*"):
        logging.logger.debug(f"Glob pattern: '{glob}'")
        return list_recipes(glob)

    def on_delete(self, sid, name):
        remove_recipe(name)
        return messages.SUCCESS
