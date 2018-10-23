import jwt
import logging
from paperboy.config import User
from paperboy.storage import UserStorage
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class UserSQL(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)

    notebooks = relationship('NotebookSQL', back_populates='user')
    jobs = relationship('JobSQL', back_populates='user')
    reports = relationship('ReportSQL', back_populates='user')

    def __repr__(self):
        return "<User(name='%s')>" % self.name


class UserSQLStorage(UserStorage):
    def __init__(self, *args, **kwargs):
        super(UserSQLStorage, self).__init__(*args, **kwargs)

    def form(self):
        return User(self.config).form()

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
