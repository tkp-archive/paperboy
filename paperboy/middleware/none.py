
class NoUserMiddleware(object):
    def __init__(self, config, db, *args, **kwargs):
        self.config = config
        self.db = db

    def process_request(self, req, resp):
        from paperboy.config import User
        req.context['user'] = User(self.config, id='1', name='anon')


class NoAuthRequiredMiddleware(object):
    def __init__(self, config, db, *args, **kwargs):
        self.config = config
        self.db = db

    def process_resource(self, req, resp, resource, params):
        pass
