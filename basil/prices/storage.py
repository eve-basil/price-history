import datetime as dt
import json

from sqlalchemy import Column, Float, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

from basil_common import logger

LOG = logger()
Base = declarative_base()


class Prices(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, index=True)
    system_id = Column(Integer, index=True)
    buy_avg = Column(Float)
    buy_min = Column(Float)
    buy_max = Column(Float)
    buy_stddev = Column(Float)
    buy_median = Column(Float)
    sell_avg = Column(Float)
    sell_min = Column(Float)
    sell_max = Column(Float)
    sell_stddev = Column(Float)
    sell_median = Column(Float)
    recorded_at = Column(DateTime, default=dt.datetime.utcnow)
    updated_at = Column(DateTime, default=dt.datetime.utcnow, index=True)

    @staticmethod
    def list(session):
        query = session.query(Prices).group_by(Prices.type_id).having(
                func.max(Prices.updated_at))
        return query.all()

    @staticmethod
    def record(session, submission):
        by_id = submission.type_id
        found = Prices.get(session, by_id)
        if found:
            if found.matches(submission):
                LOG.info('unchanged price for id [%s]', by_id)
                found.updated_at = dt.datetime.utcnow()
            else:
                LOG.info('updating price for id [%s]', by_id)
        else:
            LOG.info('creating price for id [%s]', by_id)
        session.add(submission)

    @staticmethod
    def get(session, by_id):
        return session.query(Prices).filter_by(type_id=by_id).order_by(
                Prices.updated_at.desc()).first()

    def as_dict(self):
        return {'id': self.type_id, 'system_id': self.system_id,
                'recorded_at': self.recorded_at.isoformat() + "Z",
                'updated_at': self.updated_at.isoformat() + "Z",
                'buy': {'min': self.buy_min, 'max': self.buy_max,
                        'avg': self.buy_avg, 'median': self.buy_median,
                        'stddev': self.buy_stddev},
                'sell': {'min': self.sell_min, 'max': self.sell_max,
                         'avg': self.sell_avg, 'median': self.sell_median,
                         'stddev': self.sell_stddev}}

    def json(self):
        return json.dumps(self.dict())

    @staticmethod
    def parse(by_id, data_in):
        return Prices(type_id=by_id, system_id=data_in['system_id'],
                      buy_min=data_in['buy']['min'],
                      buy_max=data_in['buy']['max'],
                      buy_avg=data_in['buy']['avg'],
                      buy_median=data_in['buy']['median'],
                      buy_stddev=data_in['buy']['stddev'],
                      sell_min=data_in['sell']['min'],
                      sell_max=data_in['sell']['max'],
                      sell_avg=data_in['sell']['avg'],
                      sell_median=data_in['sell']['median'],
                      sell_stddev=data_in['sell']['stddev'])

    def matches(self, other):
        return (self.buy_min == other.buy_min and
                self.buy_max == other.buy_max and
                self.buy_avg == other.buy_avg and
                self.buy_median == other.buy_median and
                self.buy_stddev == other.buy_stddev and
                self.sell_min == other.sell_min and
                self.sell_max == other.sell_max and
                self.sell_avg == other.sell_avg and
                self.sell_median == other.sell_median and
                self.sell_stddev == other.sell_stddev)


def migrate_db(connect_str):
    engine = create_engine(connect_str, pool_recycle=7200)
    Base.metadata.create_all(engine)
