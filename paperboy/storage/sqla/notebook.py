from paperboy.config import Notebook
from paperboy.storage import NotebookStorage
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class NotebookSQL(Base):
    __tablename__ = 'notebooks'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    userId = Column(Integer, ForeignKey('users.id'))
    user = relationship('UserSQL', back_populates='notebooks')

    jobs = relationship('JobSQL', back_populates='notebook')
    reports = relationship('ReportSQL', back_populates='notebook')

    nb = Column(String)
    privacy = Column(Integer)
    sla = Column(String, nullable=True)
    requirements = Column(String, nullable=True)
    dockerfile = Column(String, nullable=True)

    def __repr__(self):
        return "<Notebook(name='%s')>" % (self.name)


class NotebookSQLStorage(NotebookStorage):
    def form(self):
        return Notebook(self.config).form()

    def list(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'

    def detail(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'

    def store(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'
