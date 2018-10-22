# CORS middleware
from falcon_cors import CORS as CORSMiddleware

# Authentication middlewares
from falcon_helpers.middlewares.auth_required import AuthRequiredMiddleware
from falcon_helpers.middlewares.load_user import LoadUserMiddleware

# SQLAlchemy middleware
from falcon_helpers.middlewares.sqla import SQLAlchemySessionMiddleware

# Form handling middleware
from falcon_multipart.middleware import MultipartMiddleware


class DummyUserMiddleware:
    def process_request(self, req, resp):
        user_id = req.context.get('auth_token')
        req.context['user'] = user_id


class DummyAuthRequiredMiddleware:
    def __init__(self,
                 when_fails=lambda *args, **kwartgs: None):
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
