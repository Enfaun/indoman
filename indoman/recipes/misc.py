from fnmatch import filter as fnfilter
from os import listdir, removedirs
from os.path import isdir, isfile, join as path_join

from indoman.utils import constants, format_error, errors


def get_recipe(name) -> str:
    file = path_join(constants.RECIPES_DIR, name, "recipe.json")
    if isfile(file):
        return open(file).read()
    else:
        return format_error(errors.NO_SUCH_RECIPE)


def list_recipes(glob="*") -> list:
    recipes = fnfilter(listdir(constants.RECIPES_DIR), glob)
    return recipes


def remove_recipe(name: str):
    removedirs(path_join(constants.RECIPES_DIR, name))
