import json
import logging
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from paperboy.config import Report
from paperboy.config.storage import ReportListResult
from paperboy.storage import ReportStorage
from .base import Base, BaseSQLStorageMixin
from .user import UserSQL


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


class ReportSQLStorage(BaseSQLStorageMixin, ReportStorage):
    def form(self):
        return self._form(Report)

    def search(self, count, id=None, name=None, session=None, *args, **kwargs):
        return self._search(ReportSQL, count, id, name, session, *args, **kwargs)

    def list(self, req, resp, session, *args, **kwargs):
        return self._list(ReportSQL, ReportListResult, req, resp, session, *args, **kwargs)

    def detail(self, req, resp, session, *args, **kwargs):
        return self._detail(ReportSQL, req, resp, session, *args, **kwargs)

    def store(self, req, resp, session, *args, **kwargs):
        name = req.get_param('name')
        user = req.context['user']
        user_sql = session.query(UserSQL).get(int(user.id))

        nb = str(strip_outputs(nbformat.reads(req.get_param('file').file.read(), 4)))
        privacy = req.get_param('privacy') or ''
        sla = req.get_param('sla') or ''
        requirements = req.get_param('requirements') or ''
        dockerfile = req.get_param('dockerfile') or ''
        created = datetime.now()
        modified = datetime.now()

        nb = NotebookSQL(name=name,
                         userId=user.id,
                         user=user_sql,
                         nb=nb,
                         privacy=privacy,
                         sla=sla,
                         requirements=requirements,
                         dockerfile=dockerfile,
                         created=created,
                         modified=modified)
        session.add(nb)

        # generate id
        session.flush()
        session.refresh(nb)

        resp.content_type = 'application/json'
        store = nb.to_config(self.config).store()
        logging.critical("Storing notebook {}".format(name))
        resp.body = json.dumps(store)
