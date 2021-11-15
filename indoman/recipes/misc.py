from os import listdir, removedirs
from os.path import isdir, join as path_join

from indoman.utils import  constants


def list_recipes() -> list:
    [d for d in listdir(constants.RECIPES_DIR) if isdir(d)].sort()


def remove_recipe(name: str):
    removedirs(path_join(constants.RECIPES_DIR, name))
