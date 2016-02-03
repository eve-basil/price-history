import logging

import api
from common import database_connector, verify_parameters
import storage

logging = logging.getLogger(__name__)


def ensure_data(sessions):
    try:
        sessions().query(storage.Prices).first()
        sessions.remove()
    except Exception as ex:
        logging.critical('Could not connect to DB: %s', ex.message)
        exit(1)


def initialize_app():
    verify_parameters()

    db = storage.prepare_storage(database_connector())
    ensure_data(db)

    session_manager = storage.DBSessionFactory(db)
    return api.create_api([session_manager])

application = initialize_app()
