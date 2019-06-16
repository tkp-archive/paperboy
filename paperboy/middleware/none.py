from bson.objectid import ObjectId


class NoUserMiddleware(object):
    '''Dummy user authentication middleware'''
    def __init__(self, config, db, *args, **kwargs):
        self.config = config
        self.db = db

    def process_request(self, req, resp):
        '''inject anonymous user into every context'''
        from paperboy.config import UserConfig

        if self.config.backend == 'mongo':
            # must be valid id
            req.context['user'] = UserConfig(self.config, id=str(ObjectId()), name='anon')
        else:
            req.context['user'] = UserConfig(self.config, id='1', name='anon')
        req.context['token'] = 'anon'


class NoAuthRequiredMiddleware(object):
    '''Dummy no-auth-required middleware'''
    def __init__(self, config, db, *args, **kwargs):
        self.config = config
        self.db = db

    def process_resource(self, req, resp, resource, params):
        pass
