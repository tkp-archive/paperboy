import falcon
from six.moves.urllib_parse import urljoin
from mongoengine import connect
from pymongo import MongoClient


class MongoSessionMiddleware(object):
    '''variant of https://gitlab.com/skosh/falcon-helpers/blob/master/falcon_helpers/middlewares/sqla.py'''
    def __init__(self, db_url, db_name):
        self.db_url = db_url
        self.db_name = db_name

    def process_resource(self, req, resp, resource, params):
        '''initialize SQL Alchemy session and put into resource's `session` variable'''
        # Hook in ORM
        connect(self.db_name, host=self.db_url)

        # provide pymongo client if needed
        resource.session = MongoClient(self.db_url)[self.db_name]

    def process_response(self, req, resp, resource, req_succeeded):
        '''If session is successful, commit, otherwise revert'''
        pass


class MongoUserMiddleware(object):
    '''Middleware to fetch current user and put in resource's context'''
    def __init__(self, config, db, *args, **kwargs):
        self.config = config
        self.db = db

    def process_request(self, req, resp):
        '''Get user from auth token'''
        if req.context.get('auth_token') is None:
            # If the user doesnt have a token, redirect to login
            if req.path not in (urljoin(self.config.baseurl, self.config.loginurl), urljoin(self.config.baseurl, self.config.registerurl)) and \
               urljoin(self.config.baseurl, 'static') not in req.path:
                raise falcon.HTTPFound(urljoin(self.config.baseurl, self.config.loginurl))
        else:
            # try to get user

            # query for user
            user = self.db.users.detail(req.context['auth_token'], req.params)

            if user is not None:
                # user not found
                req.context['user'] = user
                if req.path in (urljoin(self.config.baseurl, self.config.loginurl), urljoin(self.config.baseurl, self.config.registerurl)):
                    raise falcon.HTTPFound(self.config.baseurl)

            elif req.path not in (urljoin(self.config.baseurl, self.config.loginurl), urljoin(self.config.baseurl, self.config.registerurl), urljoin(self.config.baseurl, self.config.logouturl)) and \
                    urljoin(self.config.baseurl, 'static') not in req.path:
                raise falcon.HTTPFound(urljoin(self.config.baseurl, self.config.loginurl))


class MongoAuthRequiredMiddleware(object):
    '''Middleware to authenticate user with sqlalchemy'''
    def __init__(self,
                 config,
                 db):
        self.config = config
        self.db = db

    def process_request(self, req, resp):
        '''if auth token present, put into context'''
        token_value = req.cookies.get('auth_token', None)
        req.context['auth_token'] = token_value

    def process_resource(self, req, resp, resource, params):
        required = getattr(resource, 'auth_required', True)
        token_value = req.context.get('auth_token', None)
        token_value = None if isinstance(token_value, Exception) else token_value

        if required and not token_value:
            raise falcon.HTTPFound(urljoin(self.config.baseurl, self.config.loginurl))
