from paperboy.config import Report
from paperboy.storage import ReportStorage
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class ReportSQL(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    userId = Column(Integer, ForeignKey('users.id'))
    user = relationship('UserSQL', back_populates='reports')

    notebookId = Column(Integer, ForeignKey('notebooks.id'))
    notebook = relationship('NotebookSQL', back_populates='reports')

    jobId = Column(Integer, ForeignKey('jobs.id'))
    job = relationship('JobSQL', back_populates='reports')

    params = Column(String)
    type = Column(String)
    output = Column(String)
    strip_code = Column(Boolean)

    def __repr__(self):
        return "<Report(name='%s')>" % (self.name)


class ReportSQLStorage(ReportStorage):
    def form(self):
        return Report(self.config).form()

    def list(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'

    def detail(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'

    def store(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'
