from logging import basicConfig, getLogger

from indoman import app_name

def init():
    global logger
    basicConfig(format="[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s")
    logger = getLogger(app_name)
