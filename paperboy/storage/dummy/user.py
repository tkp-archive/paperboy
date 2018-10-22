import falcon
from paperboy.config import User
from paperboy.storage import UserStorage


class UserDummyStorage(UserStorage):
    def form(self):
        return User(self.config).form()

    def login(self, req, resp):
        username = req.get_param('username') or ''
        password = req.get_param('password') or ''
        resp.set_cookie('auth_token', username, max_age=self.config.token_timeout, path='/', secure=not self.config.http)
        resp.status = falcon.HTTP_302
        resp.set_header('Location', self.config.baseurl)

    def logout(self, req, resp):
        resp.unset_cookie('auth_token')
        resp.status = falcon.HTTP_302
        resp.set_header('Location', self.config.baseurl)

    def list(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'

    def detail(self, req, resp):
        user_id = req.context.get('auth_token')
        if user_id:
            req.context['user'] = User(self.config, id='1', name=user_id)

    def store(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'
