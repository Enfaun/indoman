from argparse import ArgumentParser

import eventlet
from socketio import Server, WSGIApp

from indoman.utils import docker, logging, populate_namespace

logging.init()
docker.init()

static_files = {
    "/": "./frontend/index.html",
    "": "./frontend"
}
if __name__ == "__main__":
    parser = ArgumentParser(
        "indoman",
        description="Backend of Interactive Docker Manager"
        )
    parser.add_argument("--docker-url",
                        help="URL to the Docker server",
                        type=str)
    parser.add_argument("--docker-tls",
                        help="Use TLS to connect to Docker server",
                        action="store_true")
    parser.add_argument("--disable-cors",
                        help="Disable CORS check (ONLY FOR DEBUGGING!)",
                        action="store_true")
    parser.add_argument("--debug",
                        help="Show debug log",
                        action="store_true")
    parser.add_argument("--socketio-debug",
                        help="Show socket.io debug log",
                        action="store_true")
    parser.add_argument("--host",
                        help="Host to listen on",
                        type=str,
                        default="0.0.0.0")
    parser.add_argument("--port",
                        help="Port to listen on",
                        type=int,
                        default="4636")
    args = parser.parse_args()
    server_init_args = {}
    if args.disable_cors:
        server_init_args.update({"cors_allowed_origins": "*"})
    if args.debug:
        logging.logger.setLevel("DEBUG")
    if args.socketio_debug:
        server_init_args.update({"logger": True})
        server_init_args.update({"engineio_logger": True})
    sio = Server(**server_init_args)
    logging.logger.debug("Populating namespaces...")
    populate_namespace(sio)
    app = WSGIApp(sio, static_files=static_files)
    logging.logger.info("Starting up indoman...")
    eventlet.wsgi.server(eventlet.listen((args.host, args.port)), app)
else:
    sio = Server()
    populate_namespace(sio)
    app = WSGIApp(sio, static_files=static_files)
