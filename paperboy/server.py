import falcon
import gunicorn.app.base
from gunicorn.six import iteritems
from .resources import TestResource


def FalconAPI():
    api = falcon.API()
    t = TestResource()
    api.add_route('/', t)
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
