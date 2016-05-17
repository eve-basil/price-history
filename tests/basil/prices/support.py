import contextlib2 as contextlib
import os

import basil_common.db as db
import tests.basil.prices

import basil.prices.storage as storage


def testing_db_conn():
    data_path = os.path.normpath(tests.basil.prices.__path__[0] + '/../..')
    db_file = os.path.join(data_path, 'prices.db')
    with contextlib.suppress(OSError):
        os.remove(db_file)
    return "sqlite:///%s" % db_file


def session_maker():
    conn_str = testing_db_conn()
    storage.migrate_db(conn_str)
    return db.prepare_storage(connect_str=conn_str, conn_timeout=600)
