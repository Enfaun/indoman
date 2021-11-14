from docker.errors import APIError,  DockerException


def format_error(ex):
    if isinstance(ex, APIError) or isinstance(ex, IndomanError):
        ex: APIError = ex
        return {"code": ex.status_code, "is_error": True, "message": ex.explanation}
    return {"code": 500, "is_error": True, "message": "Unknown error occured"}


class IndomanError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


BAD_ZIPFILE = IndomanError(400, "BAD_ZIPFILE")
INCORRECT_RECIPE_STRUCTURE = IndomanError(400, "INCORRECT_RECIPE_STRUCTURE")
MISSING_RECIPE_FILE = IndomanError(400, "MISSING_RECIPE_FILE")
INCORRECT_RECIPE_JSON_FORMAT = IndomanError(400, "INCORRECT_RECIPE_JSON_FORMAT")
