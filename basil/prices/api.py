import json

import falcon

from basil_common.falcon_support import respond
from storage import Prices


def create_api(middleware):
    app = falcon.API(middleware=middleware)
    watches = PricesResource()
    app.add_route('/prices', watches)
    watch = PriceResource()
    app.add_route('/prices/{by_id}', watch)
    return app


class PricesResource(object):
    @staticmethod
    def on_get(req, resp):
        result = Prices.list(req.context['session'])
        found = [row.as_dict() for row in result]
        respond(resp, body=json.dumps(found))


class PriceResource(object):
    @staticmethod
    def on_get(req, resp, by_id):
        result = Prices.get(req.context['session'], by_id)
        if result:
            respond(resp, body=result.json())
        else:
            respond(resp, status=falcon.HTTP_404)

    @staticmethod
    def on_post(req, resp, by_id):
        raw_body = req.stream.read()
        if not raw_body:
            raise falcon.HTTPBadRequest('A valid JSON document is required.',
                                        '')
        try:
            body = json.loads(raw_body.decode('utf-8'))
        except UnicodeDecodeError:
            msg = 'Non-UTF8 characters found in the request body'
            raise falcon.HTTPBadRequest(msg, '')
        except ValueError as e:
            msg = 'Could not parse the body as Json: {0}. Ignoring.'.format(e)
            raise falcon.HTTPBadRequest(msg, '')

        submitted = Prices.parse(by_id, body)
        Prices.record(req.context['session'], submitted)
        resp.add_link('/prices/%s' % by_id, 'self')
        respond(resp, status=falcon.HTTP_202)
