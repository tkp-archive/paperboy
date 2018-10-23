import json
import logging
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from paperboy.config import Job, JobMetadata
from paperboy.config.storage import JobListResult
from paperboy.storage import JobStorage
from .base import Base
from .user import UserSQL
from .notebook import NotebookSQL


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

    @staticmethod
    def from_config(jb):
        # FIXME
        return JobSQL(name=jb.name,
                      userId=int(jb.user.id),
                      # user=jb.user,
                      notebookId=int(jb.notebook.id),
                      # notebook=jb.notebook,
                      reports=jb.reports,
                      start_time=jb.start_time,
                      interval=jb.interval,
                      sla=jb.sla,
                      created=jb.created,
                      modified=jb.modified)

    def to_config(self, config):
        ret = Job(config)
        ret.id = str(self.id)
        ret.name = self.name

        meta = JobMetadata()

        meta.notebook = self.notebook.to_config(self.config)
        meta.username = self.user.name
        meta.userid = str(self.user.id)

        meta.start_time = self.start_time
        meta.interval = self.interval
        meta.sla = self.sla

        meta.reports = len(self.reports)

        meta.created = self.created
        meta.modified = self.modified

        ret.meta = meta
        return ret

    def __repr__(self):
        return "<Job(name='%s')>" % (self.name)


class JobSQLStorage(JobStorage):
    def form(self):
        return Job(self.config).form()

    def list(self, req, resp, session, *args, **kwargs):
        resp.content_type = 'application/json'
        result = JobListResult()
        result.total = session.query(JobSQL).count()
        result.count = min(result.total, 25)
        result.page = 1
        result.pages = int(result.total/result.count) if result.count > 0 else 1

        nbs = session.query(JobSQL).limit(25).all()
        result.notebooks = [x.to_config(self.config) for x in nbs]
        resp.body = result.to_json(True)

    def detail(self, req, resp, session, *args, **kwargs):
        resp.content_type = 'application/json'

        id = int(req.get_param('id'))
        jb_sql = session.query(JobSQL).get(id)
        if jb_sql:
            resp.body = json.dumps(jb_sql.to_config(self.config).edit())
        else:
            resp.body = '{}'

    def store(self, req, resp, session, *args, **kwargs):
        name = req.get_param('name')

        user = req.context['user']
        user_sql = session.query(UserSQL).get(int(user.id))

        notebook = req.get_param('notebook')
        nb_sql = session.query(NotebookSQL).get(int(notebook))

        start_time = req.get_param('starttime')
        interval = req.get_param('interval') or ''
        sla = req.get_param('sla') or ''
        reports = 0
        created = datetime.now()
        modified = datetime.now()

        jb = JobSQL(name=name,
                    userId=user.id,
                    user=user_sql,
                    notebookId=notebook,
                    notebook=nb_sql,
                    reports=reports,
                    start_time=start_time,
                    interval=interval,
                    sla=sla,
                    created=created,
                    modified=modified)
        session.add(jb)

        # generate id
        session.flush()
        session.refresh(jb)

        resp.content_type = 'application/json'
        store = jb.to_config(self.config).store()
        logging.critical("Storing job {}".format(name))
        resp.body = json.dumps(store)
