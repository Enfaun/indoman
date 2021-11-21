from docker.errors import APIError,  DockerException


def format_error(ex):
    if isinstance(ex, APIError) or isinstance(ex, IndomanError):
        ex: APIError = ex
        return {"code": ex.status_code, "is_error": True, "message": ex.explanation}
    return {"code": 500, "is_error": True, "message": "Unknown error occured"}


class IndomanError(Exception):
    def __init__(self, status_code, explanation):
        self.status_code = status_code
        self.explanation = explanation


BAD_ZIPFILE = IndomanError(400, "BAD_ZIPFILE")
INCORRECT_RECIPE_STRUCTURE = IndomanError(400, "INCORRECT_RECIPE_STRUCTURE")
MISSING_RECIPE_FILE = IndomanError(400, "MISSING_RECIPE_FILE")
INCORRECT_RECIPE_JSON_FORMAT = IndomanError(400, "INCORRECT_RECIPE_JSON_FORMAT")
NO_SUCH_RECIPE = IndomanError(404, "NO_SUCH_RECIPE")
MISSING_VARIABLE = IndomanError(400, "MISSING_VARIABLE")
BAD_PREFIX_NAME = IndomanError(400, "BAD_PREFIX_NAME")
