from basil_common import configurables

import storage
from . import REQUIRED_OPTIONS

configurables.verify(REQUIRED_OPTIONS)
storage.migrate_db(configurables.database_connector())