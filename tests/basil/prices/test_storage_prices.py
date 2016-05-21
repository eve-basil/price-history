import datetime
import logging
import pytest

import basil.prices.storage as db


import support
from tests import *


# Suppress logging below error level
from tests.basil.prices import date_time_2001, fixtures

logging.getLogger('basil_common').setLevel(logging.ERROR)


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
