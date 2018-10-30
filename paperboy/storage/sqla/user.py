import jwt
import logging
from paperboy.config import User
from paperboy.storage import UserStorage
from .base import BaseSQLStorageMixin
from .models.user import UserSQL


class UserSQLStorage(BaseSQLStorageMixin, UserStorage):
    def __init__(self, *args, **kwargs):
        super(UserSQLStorage, self).__init__(*args, **kwargs)

    def status(self, *args, **kwargs):
        return {}

    def form(self):
        return self._form(User)

    def search(self, count, id=None, name=None, session=None, *args, **kwargs):
        return self._search(UserSQL, 'User', count, id, name, session, *args, **kwargs)

    def login(self, req, resp, session, *args, **kwargs):
        '''username/password -> user/token'''
        username = req.get_param('username')
        password = req.get_param('password') or ''
        user = session.query(UserSQL).filter_by(name=username, password=password).first()

        if user:
            token = jwt.encode({'id': str(user.id), 'name': user.name}, self.config.secret, algorithm='HS256').decode('ascii')
            self._do_login(token=token, req=req, resp=resp)

    def list(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'

    def detail(self, req, resp, session, *args, **kwargs):
        '''token -> user'''
        encoded = req.context.get('auth_token')
        try:
            user = jwt.decode(encoded, self.config.secret, algorithms=['HS256'])
        except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError):
            return
        req.context['user'] = User(self.config, name=user['name'], id=user['id'])

    def store(self, req, resp, session, *args, **kwargs):
        username = req.get_param('username')
        password = req.get_param('password') or ''
        user = UserSQL(name=username, password=password)

        session.add(user)  # may raise exception

        # generate id
        session.flush()
        session.refresh(user)

        token = jwt.encode({'id': str(user.id), 'name': user.name}, self.config.secret, algorithm='HS256').decode('ascii')
        logging.critical("Storing user {} {} {}".format(username, token, user.id))
        self._do_login(token=token, req=req, resp=resp)
