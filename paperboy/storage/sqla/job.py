import json
import logging
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from paperboy.config import Job, JobMetadata
from paperboy.config.storage import JobListResult
from paperboy.storage import JobStorage
from .base import Base, BaseSQLStorageMixin, justid
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
    level = Column(String, nullable=True)

    created = Column(DateTime)
    modified = Column(DateTime)

    @staticmethod
    def from_config(jb):
        # FIXME
        return JobSQL(name=jb.name,
                      userId=int(jb.user.id),
                      # user=jb.user,
                      notebookId=int(jb.notebook.id),
                      # notebook=jb.notebook,
                      reports=jb.meta.reports,
                      start_time=jb.meta.start_time,
                      interval=jb.meta.interval,
                      level=jb.meta.level,
                      created=jb.meta.created,
                      modified=jb.meta.modified)

    def to_config(self, config):
        ret = Job(config)
        ret.id = 'Job-' + str(self.id)
        ret.name = self.name

        meta = JobMetadata()
        meta.notebook = self.notebook.to_config(config)
        meta.username = self.user.name
        meta.userid = 'User-' + str(self.user.id)

        meta.start_time = self.start_time
        meta.interval = self.interval
        meta.level = self.level

        meta.reports = len(self.reports)

        meta.created = self.created
        meta.modified = self.modified

        ret.meta = meta
        return ret

    def __repr__(self):
        return "<Job(name='{}', user='{}', notebook='{}', start='{}', interval='{}'>".format(self.name, self.user, self.notebook, self.start_time, self.interval)


class JobSQLStorage(BaseSQLStorageMixin, JobStorage):
    def status(self, session, *args, **kwargs):
        return {'total': session.query(JobSQL).count(),
                'production': session.query(JobSQL).filter(JobSQL.level == 'production').count(),
                'research': session.query(JobSQL).filter(JobSQL.level == 'research').count(),
                'development': session.query(JobSQL).filter(JobSQL.level == 'development').count(),
                'personal': session.query(JobSQL).filter(JobSQL.level == 'personal').count()}

    def form(self):
        return self._form(Job)

    def search(self, count, id=None, name=None, session=None, *args, **kwargs):
        return self._search(JobSQL, 'Job', count, id, name, session, *args, **kwargs)

    def list(self, req, resp, session, *args, **kwargs):
        return self._list(JobSQL, JobListResult, 'jobs', req, resp, session, *args, **kwargs)

    def detail(self, req, resp, session, *args, **kwargs):
        return self._detail(JobSQL, req, resp, session, *args, **kwargs)

    def store(self, req, resp, session, *args, **kwargs):
        name = req.get_param('name')

        user = req.context['user']
        user_sql = session.query(UserSQL).get(int(user.id))

        notebook = req.get_param('notebook')
        nb_sql = session.query(NotebookSQL).get(int(justid(notebook)))

        start_time = datetime.strptime(req.get_param('starttime'), '%Y-%m-%dT%H:%M')
        interval = req.get_param('interval') or ''
        level = req.get_param('level') or ''
        created = datetime.now()
        modified = datetime.now()

        jb = JobSQL(name=name,
                    userId=user.id,
                    user=user_sql,
                    notebookId=notebook,
                    notebook=nb_sql,
                    start_time=start_time,
                    interval=interval,
                    level=level,
                    created=created,
                    modified=modified)
        session.add(jb)
        # generate id
        session.flush()
        session.refresh(jb)

        logging.critical("Storing job {}".format(jb))
        jobconfig = jb.to_config(self.config)
        store = jobconfig.store()

        # autogenerate reports
        reports_created = self.db.reports.autogenerate(req, resp, session, jobid=jb.id, *args, **kwargs)
        if reports_created:
            # reload to get accurate report count
            session.flush()
            session.refresh(jb)
            store = jb.to_config(self.config).store()

        resp.content_type = 'application/json'
        resp.body = json.dumps(store)
