def format_message(code, message):
    return {"code": code, "message": message}


def format_message(message):
    return format_message(200, message)


SUCCESS = format_message("SUCCESS")
RECIPE_EXTRACT_FINISHED = format_message("RECIPE_EXTRACT_FINISHED")
RECIPE_IMPORT_FINISHED = format_message("RECIPE_IMPORT_FINISHED")
CRAFT_PREPARE = format_message(201, "CRAFT_PREPARE")
CRAFT_NETWORK_CREATED = format_message(201, "CRAFT_NETWORK_CREATED")
CRAFT_CONTAINER_CREATED = format_message(201, "CRAFT_CONTAINER_CREATED")
CRAFT_FINISHED = format_message(201, "CRAFT_FINISHED")
