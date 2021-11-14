def format_message(message):
    return {"code": 200, "message": message}

SUCCESS = format_message("SUCCESS")
RECIPE_EXTRACT_FINISHED = format_message("RECIPE_EXTRACT_FINISHED")
RECIPE_IMPORT_FINISHED = format_message("RECIPE_IMPORT_FINISHED")
