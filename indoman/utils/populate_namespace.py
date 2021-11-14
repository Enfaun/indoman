from indoman import namespaces

def populate_namespace(sio):
    sio.register_namespace(namespaces.Containers("/containers"))
    sio.register_namespace(namespaces.Images("/images"))
    sio.register_namespace(namespaces.Networks("/networks"))
    sio.register_namespace(namespaces.Recipes("/recipes"))
