from paperboy.config import Job
from paperboy.storage import JobStorage
from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class JobSQL(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    owner = Column(Integer, nullable=True)  # Possibly FK in Users table

    nb_id = Column(Integer, ForeignKey('notebooks.id'))
    notebook = relationship('Notebook', back_populates='jobs')

    start_time = Column(DateTime)
    interval = Column(String)
    sla = Column(String, nullable=True)
    params = Column(JSON)
    type = Column(String)
    output = Column(String)
    strip_code = Column(Boolean)

    def __repr__(self):
        return "<Job(name='%s')>" % (self.name, self.fullname, self.password)


class JobUserSQL(Base):
    __tablename__ = 'jobs_usql'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    owner = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='jobs_usql')

    nb_id = Column(Integer, ForeignKey('notebooks_usql.id'))
    notebook = relationship('Notebook', back_populates='jobs_usql')

    start_time = Column(DateTime)
    interval = Column(String)
    sla = Column(String, nullable=True)
    params = Column(JSON)
    type = Column(String)
    output = Column(String)
    strip_code = Column(Boolean)

    def __repr__(self):
        return "<Job(name='%s')>" % (self.name, self.fullname, self.password)


class JobSQLStorage(JobStorage):
    def form(self):
        return Job(self.config).form()

    def list(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'

    def detail(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'

    def store(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'
