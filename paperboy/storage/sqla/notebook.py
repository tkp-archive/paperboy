import json
import nbformat
import logging
from datetime import datetime
from paperboy.config import Notebook
from paperboy.config.storage import NotebookListResult
from paperboy.storage import NotebookStorage
from .base import BaseSQLStorageMixin
from .models.user import UserSQL
from .models.notebook import NotebookSQL
from ..utils import strip_outputs


class NotebookSQLStorage(BaseSQLStorageMixin, NotebookStorage):
    def status(self, session, *args, **kwargs):
        return {'total': session.query(NotebookSQL).count(),
                'public': session.query(NotebookSQL).filter(NotebookSQL.level == 'public').count(),
                'private': session.query(NotebookSQL).filter(NotebookSQL.privacy == 'private').count()}

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
        level = req.get_param('level') or ''
        requirements = req.get_param('requirements') or ''
        dockerfile = req.get_param('dockerfile') or ''
        created = datetime.now()
        modified = datetime.now()

        nb = NotebookSQL(name=name,
                         userId=int(user.id),
                         user=user_sql,
                         notebook=notebook,
                         privacy=privacy,
                         level=level,
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
