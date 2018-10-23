import json
import logging
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from paperboy.config import Report
from paperboy.config.storage import ReportListResult
from paperboy.storage import ReportStorage
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

    def list(self, req, resp, *args, **kwargs):
        resp.content_type = 'application/json'
        result = ReportListResult()
        result.page = 1
        result.pages = 1
        result.count = 0
        result.total = 0
        result.reports = []
        resp.body = result.to_json(True)

    def detail(self, req, resp, *args, **kwargs):
        resp.content_type = 'application/json'
        details = Report.from_json(
            {'name': 'TestReport1',
             'id': 'Report-1',
             'meta': {
                'created': '10/14/2018 04:50:33',
                'run': '10/14/2018 18:25:31',
                 }},
            self.config).edit()
        resp.body = json.dumps(details)

    def store(self, req, resp, *args, **kwargs):
        name = req.get_param('name')
        nb_name = req.get_param('notebook')
        rp_name = req.get_param('report')
        resp.content_type = 'application/json'

        store = Report.from_json(
            {'name': 'TestReport1',
             'id': 'Report-1',
             'meta': {
                'created': '10/14/2018 04:50:33',
                'run': '10/14/2018 18:25:31',
                 }},
            self.config).store()
        logging.critical("Storing job {}".format(name))
        resp.body = json.dumps(store)
