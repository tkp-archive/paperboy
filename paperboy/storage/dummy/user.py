import logging
from paperboy.config import User
from paperboy.storage import UserStorage


class UserDummyStorage(UserStorage):
    def form(self, *args, **kwargs):
        return User(self.config).form()

    def login(self, req, resp, *args, **kwargs):
        username = req.get_param('username') or ''
        password = req.get_param('password') or ''
        self._do_login(token=username, req=req, resp=resp)

    def list(self, req, resp, *args, **kwargs):
        resp.content_type = 'application/json'
        resp.body = '{}'

    def detail(self, req, resp, *args, **kwargs):
        req.context['user'] = User(name=req.context['auth_token'], id='1')

    def store(self, req, resp, *args, **kwargs):
        username = req.get_param('username') or ''
        logging.critical("Storing user {}".format(username))

        self._do_login(token=username, req=req, resp=resp)
