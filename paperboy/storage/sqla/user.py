import falcon
import logging
from paperboy.config import User
from paperboy.storage import UserStorage
from sqlalchemy import Column, Integer, String
from .base import Base


class UserSQL(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s')>" % (self.name, self.password)


class UserSQLStorage(UserStorage):
    def form(self):
        return User(self.config).form()

    def login(self, req, resp):
        username = req.get_param('username')
        password = req.get_param('password')
        user = self.session.query(UserSQL).filter_by(name=username, password=password).first()
        if user:
            # FIXME
            self._do_login(token=username, req=req, resp=resp)
        else:
            resp.status = falcon.HTTP_302
            resp.set_header('Location', self.config.registerurl)

    def list(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'

    def detail(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'

    def store(self, req, resp):
        username = req.get_param('username')
        password = req.get_param('password')
        user = UserSQL(name=username, password=password)
        logging.critical("Storing user {}".format(username))
        self.session.add(user)  # may raise exception
        self.session.commit()

        resp.content_type = 'application/json'
        resp.body = '{}'
