import logging


logging.basicConfig(
    format='[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S +0000', level=logging.DEBUG
    )
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

JITA = 30000142
DODIXIE = 30002659
AMARR = 30002187
