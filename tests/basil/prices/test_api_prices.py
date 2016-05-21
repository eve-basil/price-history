import falcon
import pytest

import basil_common.db as db
from basil.prices import api
import basil.prices.storage as storage
import support
from tests import *
from tests.basil.prices import fixtures


@pytest.fixture()
def with_fixtures():
    pre_sess = support.session_maker()()
    for f in fixtures:
        pre_sess.add(storage.Prices(**f))
    pre_sess.commit()
    pre_sess.close()


@pytest.fixture(scope="module")
def app():
    middleware = [db.SessionManager(support.session_maker())]
    return api.create_api(middleware)

application = app()


def test_get_all(client, with_fixtures):
    resp = client.get('/prices')
    assert_that(resp, has_property('status', equal_to(falcon.HTTP_OK)))
    assert_that(resp.json, has_length(2))
    assert_that(resp.json[0], has_entry('id', 100))


def test_get_by_id(client, with_fixtures):
    resp = client.get('/prices/102')
    assert_that(resp, has_property('status', equal_to(falcon.HTTP_OK)))
    assert_that(resp.json, has_entry('id', 102))


def test_get_by_str_id(client):
    resp = client.get('/prices/thirtyfour')
    assert_that(resp, has_property('status',
                                   equal_to(falcon.HTTP_BAD_REQUEST)))


def test_get_by_unknown_id(client):
    resp = client.get('/prices/99999999')
    assert_that(resp, has_property('status',
                                   equal_to(falcon.HTTP_NOT_FOUND)))


def test_put_by_str_id(client):
    resp = client.put('/prices/thirtyfour', None)
    assert_that(resp, has_property('status',
                                   equal_to(falcon.HTTP_METHOD_NOT_ALLOWED)))


def test_post_blank_by_id(client):
    resp = client.post('/prices/34', None)
    assert_that(resp, has_property('status',
                                   equal_to(falcon.HTTP_BAD_REQUEST)))


def test_post_by_id(client):
    payload = {'system_id': 4005001,
               'buy': {'min': 11.22, 'max': 11.33, 'avg': 15.15,
                       'median': 20.20, 'stddev': 9.61},
               'sell': {'min': 54.54, 'max': 52.52, 'avg': 57.57,
                        'median': 23.23, 'stddev': 8.50}}

    json_header = {'Content-Type': 'application/json'}
    resp = client.post('/prices/34', payload, headers=json_header)

    assert_that(resp, has_property('status',
                                   equal_to(falcon.HTTP_ACCEPTED)))
