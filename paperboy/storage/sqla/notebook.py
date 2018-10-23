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
from .base import Base
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

    nb = Column(String)
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
                           nb=nb.nb,
                           privacy=nb.privacy,
                           sla=nb.sla,
                           requirements=nb.requirements,
                           dockerfile=nb.dockerfile,
                           created=nb.created,
                           modified=nb.modified)

    def to_config(self, config):
        ret = Notebook(config)
        ret.id = str(self.id)
        ret.name = self.name

        meta = NotebookMetadata()

        meta.username = self.user.name
        meta.userid = str(self.user.id)

        meta.nb = self.nb
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
        return "<Notebook(name='%s')>" % (self.name)


class NotebookSQLStorage(NotebookStorage):
    def form(self):
        return Notebook(self.config).form()

    def list(self, req, resp, session, *args, **kwargs):
        resp.content_type = 'application/json'
        result = NotebookListResult()
        result.total = session.query(NotebookSQL).count()
        result.count = min(result.total, 25)
        result.page = 1
        result.pages = int(result.total/result.count) if result.count > 0 else 1

        nbs = session.query(NotebookSQL).limit(25).all()
        result.notebooks = [x.to_config(self.config) for x in nbs]
        resp.body = result.to_json(True)

    def detail(self, req, resp, session, *args, **kwargs):
        resp.content_type = 'application/json'

        id = int(req.get_param('id'))
        nb_sql = session.query(NotebookSQL).get(id)
        if nb_sql:
            resp.body = json.dumps(nb_sql.to_config(self.config).edit())
        else:
            resp.body = '{}'

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
                         userId=int(user.id),
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
