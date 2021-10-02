import traceback

from docker.errors import APIError,  DockerException

def format_error(ex: DockerException):
    if isinstance(ex, APIError):
        ex: APIError = ex
        return {"error": ex.status_code, "message": ex.explanation}
    return {"error": 500, "message": "Unknown error occured"}
