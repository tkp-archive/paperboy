import falcon
import gunicorn.app.base
from gunicorn.six import iteritems
from .resources import StaticResource, HTMLResource
from .middleware import HandleCORS


def FalconAPI():
    api = falcon.API(middleware=[HandleCORS()])
    html = HTMLResource()
    static = StaticResource()

    api.add_route('/', html)
    api.add_route('/index.html', html)
    api.add_sink(static.on_get, prefix='/static')
    return api


class FalconGunicorn(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(FalconGunicorn, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def main():
    options = {
        'bind': '0.0.0.0:8080',
        'workers': 2
    }
    FalconGunicorn(FalconAPI(), options).run()

if __name__ == '__main__':
    main()
