from indoman import namespaces

def populate_namespace(sio):
    sio.register_namespace(namespaces.Containers("/containers"))
