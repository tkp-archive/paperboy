from paperboy.config import Report
from paperboy.storage import ReportStorage
from sqlalchemy import Column, Integer, String, JSON, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class ReportSQL(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    owner = Column(Integer, nullable=True)  # Possibly FK in Users table

    nb_id = Column(Integer, ForeignKey('notebooks.id'))
    notebook = relationship('Notebook', back_populates='reports')
    jb_id = Column(Integer, ForeignKey('jobs.id'))
    job = relationship('Job', back_populates='reports')

    params = Column(JSON)
    type = Column(String)
    output = Column(String)
    strip_code = Column(Boolean)

    def __repr__(self):
        return "<Report(name='%s')>" % (self.name, self.fullname, self.password)


class ReportUserSQL(Base):
    __tablename__ = 'reports_usql'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    owner = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='reports_usql')

    nb_id = Column(Integer, ForeignKey('notebooks_usql.id'))
    notebook = relationship('Notebook', back_populates='reports_usql')
    jb_id = Column(Integer, ForeignKey('jobs_usql.id'))
    job = relationship('Job', back_populates='reports_usql')

    params = Column(JSON)
    type = Column(String)
    output = Column(String)
    strip_code = Column(Boolean)

    def __repr__(self):
        return "<Report(name='%s')>" % (self.name, self.fullname, self.password)


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
