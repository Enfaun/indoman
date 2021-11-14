from json import load as json_load, JSONDecodeError
from os import mkdir, listdir, removedirs
from os.path import isdir, join as path_join, isfile
from shutil import move
from zipfile import ZipFile, BadZipfile

from socketio import Namespace

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
            tmp_dir = self.unpack_zip(zip_filename)
            self.send(messages.RECIPE_EXTRACT_FINISHED, room)
            self.parse_recipe(tmp_dir)
            self.send(messages.RECIPE_IMPORT_FINISHED, room)
        except BadZipfile:
            self.send(errors.BAD_ZIPFILE, room)
        except Exception as e:
            self.send(format_error(e))
        finally:
            self.leave_room(sid, room)

    def unpack_zip(self, zip_filename):
        zipfile = ZipFile(zip_filename)
        infolist = zipfile.infolist()
        tmp_dir = path_join(constants.TEMP_DIR, f"{zip_filename}-extracted")
        mkdir(tmp_dir)
        zipfile.extractall(tmp_dir)

        if isfile(path_join(tmp_dir, "recipe.json")):
            return tmp_dir
        else:
            tmp_dir_content = listdir(tmp_dir)
            if len(tmp_dir_content) == 1:
                return path_join(tmp_dir, tmp_dir_content[0])
            else:
                raise errors.INCORRECT_RECIPE_STRUCTURE

    def parse_recipe(self, directory):
        recipe = path_join(directory, "recipe.json")
        if not isfile(recipe):
            raise errors.MISSING_RECIPE_FILE
        recipefp = open(recipe)
        try:
            recipe_json = json_load(recipefp)
            name = recipe_json["name"]
            new_recipe_path = path_join(constants.RECIPES_DIR, name)
            move(directory, new_recipe_path + "/")
        except (JSONDecodeError, KeyError):
            raise errors.INCORRECT_RECIPE_JSON_FORMAT
        finally:
            recipefp.close()

    def on_craft(self, sid, recipe, prefix, config):
        pass

    def on_list(self, sid):
        return [d for d in listdir(constants.RECIPES_DIR) if isdir(d)].sort()

    def on_delete(self, sid, name):
        removedirs(path_join(constants.RECIPES_DIR, name))
        return messages.SUCCESS
