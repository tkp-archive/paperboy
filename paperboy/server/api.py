import falcon
from ..resources import StaticResource, HTMLResource, StatusResource
from ..middleware import HandleCORS

API = '/api/v1/'


def FalconAPI():
    api = falcon.API(middleware=[HandleCORS()])

    # Static resources
    html = HTMLResource()
    static = StaticResource()
    api.add_route('/', html)
    api.add_route('/index.html', html)
    api.add_sink(static.on_get, prefix='/static')

    # Routes
    status = StatusResource()
    api.add_route(API + 'status', status)
    return api
