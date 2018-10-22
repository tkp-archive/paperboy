import logging
from paperboy.config import User
from paperboy.storage import UserStorage


class UserDummyStorage(UserStorage):
    def form(self):
        return User(self.config).form()

    def login(self, req, resp):
        username = req.get_param('username') or ''
        password = req.get_param('password') or ''
        self._do_login(token=username, req=req, resp=resp)

    def list(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'

    def detail(self, req, resp):
        user_id = req.context.get('auth_token')
        if user_id:
            req.context['user'] = User(self.config, id='1', name=user_id)

    def store(self, req, resp):
        username = req.get_param('username') or ''
        self._do_login(token=username, req=req, resp=resp)
        logging.critical("Storing user {}".format(username))
        resp.content_type = 'application/json'
        resp.body = '{}'
