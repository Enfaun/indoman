def format_message(code, message):
    return {"code": code, "message": message}


SUCCESS = format_message(200, "SUCCESS")
RECIPE_EXTRACT_FINISHED = format_message(200, "RECIPE_EXTRACT_FINISHED")
RECIPE_IMPORT_FINISHED = format_message(200, "RECIPE_IMPORT_FINISHED")
CRAFT_PREPARE = format_message(201, "CRAFT_PREPARE")
CRAFT_PULLING_IMAGE = format_message(201, "CRAFT_PULLING_IMAGE")
CRAFT_NETWORK_CREATED = format_message(201, "CRAFT_NETWORK_CREATED")
CRAFT_CONTAINER_CREATED = format_message(201, "CRAFT_CONTAINER_CREATED")
CRAFT_FINISHED = format_message(201, "CRAFT_FINISHED")
