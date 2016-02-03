import common
import storage


common.verify_parameters()
storage.migrate_db(common.database_connector())