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
        pass

    def logout(self, req, resp):
        pass

    def list(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'

    def detail(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'

    def store(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'
