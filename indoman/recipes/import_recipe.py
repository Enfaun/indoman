from json import load as json_load, JSONDecodeError
from os import mkdir, listdir, removedirs
from os.path import join as path_join, isfile
from re import  compile as re_compile
from shutil import move
from zipfile import ZipFile

from indoman.utils import errors, constants


def unpack_zip(zip_filename):
    zipfile = ZipFile(zip_filename)
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


def parse_recipe(directory):
    recipe = path_join(directory, "recipe.json")
    if not isfile(recipe):
        raise errors.MISSING_RECIPE_FILE
    recipefp = open(recipe)
    try:
        recipe_json = json_load(recipefp)
        name_re = re_compile("[a-z_]+]")
        name = recipe_json["canonical_id"]
        if not name_re.match(name):
            raise errors.INCORRECT_RECIPE_JSON_FORMAT
        new_recipe_path = path_join(constants.RECIPES_DIR, name)
        move(directory, new_recipe_path + "/")
    except (JSONDecodeError, KeyError):
        removedirs(directory)
        raise errors.INCORRECT_RECIPE_JSON_FORMAT
    finally:
        recipefp.close()
