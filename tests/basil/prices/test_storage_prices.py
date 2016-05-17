import datetime
import logging
import pytest

import basil.prices.storage as db


import support
from tests import *


# Suppress logging below error level
logging.getLogger('basil_common').setLevel(logging.ERROR)

date_time_1999 = datetime.datetime.utcfromtimestamp(946684799)
date_time_2001 = datetime.datetime.utcfromtimestamp(978310923)
date_time_2012_may = datetime.datetime.utcfromtimestamp(1336197305)
date_time_2012_jun = datetime.datetime.utcfromtimestamp(1339869960)

fixtures = [{'type_id': 100, 'system_id': 22, 'buy_avg': 45.12,
             'buy_min': 39.83, 'buy_max': 51.36, 'buy_stddev': 2.93,
             'buy_median': 47.04, 'sell_avg': 96.82, 'sell_min': 72.44,
             'sell_max': 142.25, 'sell_stddev': 3.07, 'sell_median': 98.36,
             'recorded_at': date_time_1999, 'updated_at': date_time_1999},
            {'type_id': 100, 'system_id': 22, 'buy_avg': 46.46,
             'buy_min': 40.03, 'buy_max': 54.82, 'buy_stddev': 2.19,
             'buy_median': 41.89, 'sell_avg': 98.21, 'sell_min': 74.30,
             'sell_max': 149.81, 'sell_stddev': 3.32, 'sell_median': 94.15,
             'recorded_at': date_time_2001, 'updated_at': date_time_2001},
            {'type_id': 102, 'system_id': 22, 'buy_avg': 7.07,
             'buy_min': 5.98, 'buy_max': 9.1, 'buy_stddev': 0.11,
             'buy_median': 7.50, 'sell_avg': 9.44, 'sell_min': 8.95,
             'sell_max': 10.17, 'sell_stddev': 0.20, 'sell_median': 9.84,
             'recorded_at': date_time_2001, 'updated_at': date_time_2001}]


# destroy the DB and session for each test to ensure no data cruft accumulates
@pytest.fixture()
def session():
    maker = support.session_maker()
    pre_sess = maker()
    for f in fixtures:
        pre_sess.add(db.Prices(**f))
    pre_sess.commit()
    pre_sess.close()

    return maker()


def test_get_by_unknown_id(session):
    p = db.Prices.get(session, 17)
    assert_that(p, is_(none()))


def test_get_known_id(session):
    p = db.Prices.get(session, 100)
    assert_that(p, has_property('buy_median', equal_to(41.89)))
    assert_that(p, has_property('recorded_at', equal_to(date_time_2001)))
    assert_that(p, has_property('updated_at', equal_to(date_time_2001)))


def test_list(session):
    listed = db.Prices.list(session)
    assert_that(listed, has_length(2))
    assert_that([p.type_id for p in listed], equal_to([100, 102]))


def test_matches_ignores_dates(session):
    expected = db.Prices(**fixtures[1])
    expected.recorded_at = datetime.datetime.utcnow
    expected.updated_at = datetime.datetime.utcnow
    actual = db.Prices.get(session, 100)
    assert_that(expected.matches(actual), is_(True))


def test_matches_rejects_mismatch(session):
    expected = db.Prices(**fixtures[1])
    expected.recorded_at = datetime.datetime.utcnow
    expected.updated_at = datetime.datetime.utcnow
    actual = db.Prices.get(session, 102)
    assert_that(expected.matches(actual), is_not(True))


def test_record_unchanged_prices(session):
    now = datetime.datetime.utcnow()
    p = db.Prices.get(session, 100)
    original_update = p.updated_at

    db.Prices.record(session, p)
    session.commit()
    q = db.Prices.get(session, 100)

    assert_that(q, has_property('recorded_at', equal_to(p.recorded_at)))
    assert_that(q, has_property('updated_at', greater_than(original_update)))
    assert_that(q, has_property('updated_at', greater_than_or_equal_to(now)))
