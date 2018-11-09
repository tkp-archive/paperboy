import nbformat
import logging
from datetime import datetime
from paperboy.config import NotebookConfig
from paperboy.storage import NotebookStorage
from sqlalchemy import or_
from .base import BaseSQLStorageMixin
from .models.user import UserSQL
from .models.notebook import NotebookSQL
from ..utils import strip_outputs


class NotebookSQLStorage(BaseSQLStorageMixin, NotebookStorage):
    def status(self, user, params, session, *args, **kwargs):
        base = session.query(NotebookSQL) \
            .filter(or_(NotebookSQL.userId.like((user.id)),
                        (hasattr(NotebookSQL, 'privacy') and NotebookSQL.privacy == 'public')))

        return {'total': base.count(),
                'public': base.filter(NotebookSQL.level == 'public').count(),
                'private': base.filter(NotebookSQL.privacy == 'private').count()}

    def form(self):
        return self._form(NotebookConfig)

    def search(self, user, params, session, *args, **kwargs):
        return self._search(NotebookSQL, 'Notebook', user, params, session, *args, **kwargs)

    def list(self, user, params, session, *args, **kwargs):
        return self._list(NotebookSQL, 'notebooks', user, params, session, *args, **kwargs)

    def detail(self, user, params, session, *args, **kwargs):
        return self._detail(NotebookSQL, user, params, session, *args, **kwargs)

    def store(self, user, params, session, *args, **kwargs):
        name = params.get('name')
        user_sql = session.query(UserSQL).get(int(user.id))

        notebook = nbformat.writes(strip_outputs(nbformat.reads(params.get('file').file.read(), 4)))
        privacy = params.get('privacy') or ''
        level = params.get('level') or ''
        requirements = params.get('requirements') or ''
        dockerfile = params.get('dockerfile') or ''
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

        store = nb.to_config(self.config).store()
        logging.critical("Storing notebook {}".format(nb))
        return store
