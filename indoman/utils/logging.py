from logging import basicConfig, getLogger, Logger

from indoman import app_name


logger: Logger

def init():
    global logger
    basicConfig(format="[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s")
    logger = getLogger(app_name)
