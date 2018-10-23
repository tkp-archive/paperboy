import json
import logging
from random import randint, choice
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from paperboy.config import Job
from paperboy.config.storage import JobListResult
from paperboy.storage import JobStorage
from .base import Base


class JobSQL(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    userId = Column(Integer, ForeignKey('users.id'))
    user = relationship('UserSQL', back_populates='jobs')

    notebookId = Column(Integer, ForeignKey('notebooks.id'))
    notebook = relationship('NotebookSQL', back_populates='jobs')

    reports = relationship('ReportSQL', back_populates='job')

    start_time = Column(DateTime)
    interval = Column(String)
    sla = Column(String, nullable=True)
    params = Column(String)
    type = Column(String)
    output = Column(String)
    strip_code = Column(Boolean)

    def __repr__(self):
        return "<Job(name='%s')>" % (self.name)


class JobSQLStorage(JobStorage):
    def form(self):
        return Job(self.config).form()

    def list(self, req, resp, *args, **kwargs):
        resp.content_type = 'application/json'
        result = JobListResult()
        result.page = 1
        result.pages = 1
        result.count = 0
        result.total = 0
        result.jobs = []
        resp.body = result.to_json(True)

    def detail(self, req, resp, *args, **kwargs):
        resp.content_type = 'application/json'
        store = Job.from_json(
                        {'name': 'TestJob1',
                         'id': 'Job-1',
                         'meta': {
                            # 'notebook': 'TestNotebook',
                            # 'notebookid': 'Notebook-%d' % i,
                            'owner': 'TestOwner',
                            'reports': randint(1, 1000),
                            'interval': choice(['minutely',
                                                '5 minutes',
                                                '10 minutes',
                                                '30 minutes',
                                                'hourly',
                                                '2 hours',
                                                '3 hours',
                                                '6 hours',
                                                '12 hours',
                                                'daily',
                                                'weekly',
                                                'monthly']),
                            'created': '10/14/2018 04:50:33',
                            'modified': '10/14/2018 18:25:31'}},
                        self.config).edit()
        resp.body = json.dumps(store)

    def store(self, req, resp, *args, **kwargs):
        name = req.get_param('name')
        nb_name = req.get_param('notebook')
        resp.content_type = 'application/json'
        store = Job.from_json(
                        {'name': 'TestJob1',
                         'id': 'Job-1',
                         'meta': {
                            # 'notebook': 'TestNotebook',
                            # 'notebookid': 'Notebook-%d' % i,
                            'owner': 'TestOwner',
                            'reports': randint(1, 1000),
                            'interval': choice(['minutely',
                                                '5 minutes',
                                                '10 minutes',
                                                '30 minutes',
                                                'hourly',
                                                '2 hours',
                                                '3 hours',
                                                '6 hours',
                                                '12 hours',
                                                'daily',
                                                'weekly',
                                                'monthly']),
                            'created': '10/14/2018 04:50:33',
                            'modified': '10/14/2018 18:25:31',
                             }},
                        self.config).store()
        logging.critical("Storing job {}".format(name))
        resp.body = json.dumps(store)
