import falcon
from six.moves.urllib_parse import urljoin


class SQLAlchemySessionMiddleware(object):
    '''variant of https://gitlab.com/skosh/falcon-helpers/blob/master/falcon_helpers/middlewares/sqla.py'''
    def __init__(self, sessionmaker=None):
        self.sessionmaker = sessionmaker

    def process_resource(self, req, resp, resource, params):
        self.session = self.sessionmaker()
        resource.session = self.session

    def process_response(self, req, resp, resource, req_succeeded):
        if not hasattr(resource, 'session'):
            return

        try:
            if not req_succeeded:
                self.session.rollback()
            else:
                self.session.commit()
        except Exception:
            self.session.remove()
            raise
        finally:
            self.session.close()


class SQLUserMiddleware(object):
    def __init__(self, config, db, *args, **kwargs):
        self.config = config
        self.db = db

    def process_request(self, req, resp):
        if req.context.get('auth_token') is None:
            if req.path not in (urljoin(self.config.baseurl, self.config.loginurl), urljoin(self.config.baseurl, self.config.registerurl)) and \
               urljoin(self.config.baseurl, 'static') not in req.path:
                raise falcon.HTTPFound(urljoin(self.config.baseurl, self.config.loginurl))
        else:
            # try to get user
            session = self.config.storage.sessionmaker()
            user = self.db.users.detail(req.context['auth_token'], req.params, session)
            if user is not None:
                req.context['user'] = user
                if req.path in (urljoin(self.config.baseurl, self.config.loginurl), urljoin(self.config.baseurl, self.config.registerurl)):
                    raise falcon.HTTPFound(self.config.baseurl)

            elif req.path not in (urljoin(self.config.baseurl, self.config.loginurl), urljoin(self.config.baseurl, self.config.registerurl), urljoin(self.config.baseurl, self.config.logouturl)) and \
                    urljoin(self.config.baseurl, 'static') not in req.path:
                raise falcon.HTTPFound(urljoin(self.config.baseurl, self.config.loginurl))


class SQLAuthRequiredMiddleware(object):
    def __init__(self,
                 config,
                 db):
        self.config = config
        self.db = db

    def process_request(self, req, resp):
        token_value = req.cookies.get('auth_token', None)
        req.context['auth_token'] = token_value

    def process_resource(self, req, resp, resource, params):
        required = getattr(resource, 'auth_required', True)
        token_value = req.context.get('auth_token', None)
        token_value = None if isinstance(token_value, Exception) else token_value

        if required and not token_value:
            raise falcon.HTTPFound(urljoin(self.config.baseurl, self.config.loginurl))
