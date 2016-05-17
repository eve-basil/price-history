import api
from basil_common import configurables, db, logger
from . import REQUIRED_OPTIONS
import storage

LOG = logger()


def ensure_data(session):
    try:
        first = session.query(storage.Prices).first()
        session.close()
        if not first:
            raise SystemExit('Cannot connect to Prices DB')
    except ImportError as ex:
        LOG.fatal(ex.message)
        raise
    else:
        LOG.info('DB Connected')


def initialize_app():
    configurables.verify(REQUIRED_OPTIONS)

    db_store = db.prepare_storage(configurables.database_connector(), 7200)
    ensure_data(db_store())

    session_manager = db.SessionManager(db_store)
    app = api.create_api([session_manager])

    # Add a different root error handler based on: are we in production or not
    error_handler = configurables.root_error_handler()
    app.add_error_handler(Exception, error_handler)

    return app


application = initialize_app()
