import falcon
from ..resources import StaticResource, HTMLResource
from ..middleware import HandleCORS


def FalconAPI():
    api = falcon.API(middleware=[HandleCORS()])
    html = HTMLResource()
    static = StaticResource()

    api.add_route('/', html)
    api.add_route('/index.html', html)
    api.add_sink(static.on_get, prefix='/static')
    return api
