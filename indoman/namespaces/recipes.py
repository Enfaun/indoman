from json import load as json_load, JSONDecodeError
from os import mkdir, listdir, removedirs
from os.path import isdir, join as path_join, isfile
from shutil import move
from zipfile import ZipFile, BadZipfile

from socketio import Namespace

from indoman.recipes import import_recipe, list_recipes, remove_recipe
from indoman.utils import docker, logging, format_error, errors, constants, messages


class Recipes(Namespace):
    def on_connect(self, sid, environ):
        pass

    def on_disconnect(self, sid):
        pass

    def on_upload(self, sid, data):
        if not isdir(constants.RECIPES_DIR): mkdir(constants.RECIPES_DIR)
        logging.logger.info(f"{sid} uploading recipes...")
        logging.logger.debug(type(sid))
        zip_filename = f"recipes/tmp-{sid}.zip"
        file = open(zip_filename, "wb")
        file.write(data)
        room = zip_filename + "-room"
        self.enter_room(sid, room)
        try:
            tmp_dir = import_recipe.unpack_zip(zip_filename)
            self.send(messages.RECIPE_EXTRACT_FINISHED, room)
            import_recipe.parse_recipe(tmp_dir)
            self.send(messages.RECIPE_IMPORT_FINISHED, room)
        except BadZipfile:
            self.send(errors.BAD_ZIPFILE, room)
        except Exception as e:
            self.send(format_error(e))
        finally:
            self.leave_room(sid, room)

    def on_craft(self, sid, recipe, prefix, config):
        pass

    def on_list(self, sid):
        return list_recipes()

    def on_delete(self, sid, name):
        remove_recipe(name)
        return messages.SUCCESS
