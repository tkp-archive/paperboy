
class DummyUserMiddleware(object):
    def __init__(self, config, db, *args, **kwargs):
        self.config = config
        self.db = db

    def process_request(self, req, resp):
        self.db.users.detail(req, resp)


class DummyAuthRequiredMiddleware(object):
    def __init__(self,
                 config,
                 db,
                 when_fails=lambda *args, **kwargs: None):
        self.config = config
        self.db = db
        self.failed_action = when_fails

    def process_request(self, req, resp):
        token_value = req.cookies.get('auth_token', None)
        req.context['auth_token'] = token_value

    def process_resource(self, req, resp, resource, params):
        required = getattr(resource, 'auth_required', True)
        token_value = req.context.get('auth_token', None)
        token_value = None if isinstance(token_value, Exception) else token_value
        if required and not token_value:
            return self.failed_action(req=req, resp=resp, token_value=token_value)
