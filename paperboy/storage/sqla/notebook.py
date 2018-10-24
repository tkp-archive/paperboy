import json
import nbformat
import logging
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from paperboy.config import Notebook, NotebookMetadata
from paperboy.config.storage import NotebookListResult
from paperboy.storage import NotebookStorage
from .base import Base, BaseSQLStorageMixin
from .user import UserSQL
from ..utils import strip_outputs


class NotebookSQL(Base):
    __tablename__ = 'notebooks'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    userId = Column(Integer, ForeignKey('users.id'))
    user = relationship('UserSQL', back_populates='notebooks')

    jobs = relationship('JobSQL', back_populates='notebook')
    reports = relationship('ReportSQL', back_populates='notebook')

    notebook = Column(String)
    privacy = Column(String, nullable=True)
    sla = Column(String, nullable=True)
    requirements = Column(String, nullable=True)
    dockerfile = Column(String, nullable=True)

    created = Column(DateTime)
    modified = Column(DateTime)

    @staticmethod
    def from_config(nb):
        # FIXME
        return NotebookSQL(name=nb.name,
                           userId=int(nb.user.id),
                           notebook=nb.notebook,
                           privacy=nb.privacy,
                           sla=nb.sla,
                           requirements=nb.requirements,
                           dockerfile=nb.dockerfile,
                           created=nb.created,
                           modified=nb.modified)

    def to_config(self, config):
        ret = Notebook(config)
        ret.id = 'Notebook-' + str(self.id)
        ret.name = self.name

        meta = NotebookMetadata()

        meta.username = self.user.name
        meta.userid = 'User-' + str(self.user.id)

        meta.notebook = self.notebook
        meta.privacy = self.privacy
        meta.sla = self.sla

        meta.requirements = self.requirements
        meta.dockerfile = self.dockerfile

        meta.jobs = len(self.jobs)
        meta.reports = len(self.reports)

        meta.created = self.created
        meta.modified = self.modified

        ret.meta = meta
        return ret

    def __repr__(self):
        return "<Notebook(name='{}', user='{}', privacy='{}', sla='{}'>".format(self.name, self.user, self.privacy, self.sla)


class NotebookSQLStorage(BaseSQLStorageMixin, NotebookStorage):
    def form(self):
        return self._form(Notebook)

    def search(self, count, id=None, name=None, session=None, *args, **kwargs):
        return self._search(NotebookSQL, 'Notebook', count, id, name, session, *args, **kwargs)

    def list(self, req, resp, session, *args, **kwargs):
        return self._list(NotebookSQL, NotebookListResult, 'notebooks', req, resp, session, *args, **kwargs)

    def detail(self, req, resp, session, *args, **kwargs):
        return self._detail(NotebookSQL, req, resp, session, *args, **kwargs)

    def store(self, req, resp, session, *args, **kwargs):
        name = req.get_param('name')
        user = req.context['user']
        user_sql = session.query(UserSQL).get(int(user.id))

        notebook = nbformat.writes(strip_outputs(nbformat.reads(req.get_param('file').file.read(), 4)))
        privacy = req.get_param('privacy') or ''
        sla = req.get_param('sla') or ''
        requirements = req.get_param('requirements') or ''
        dockerfile = req.get_param('dockerfile') or ''
        created = datetime.now()
        modified = datetime.now()

        nb = NotebookSQL(name=name,
                         userId=int(user.id),
                         user=user_sql,
                         notebook=notebook,
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
        logging.critical("Storing notebook {}".format(nb))
        resp.body = json.dumps(store)
