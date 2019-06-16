import nbformat
import logging
from datetime import datetime
from paperboy.config import NotebookConfig
from paperboy.storage import NotebookStorage
from mongoengine.queryset.visitor import Q
from .base import BaseMongoStorageMixin, justid
from .models.user import UserMongo
from .models.notebook import NotebookMongo
from ..utils import strip_outputs


class NotebookMongoStorage(BaseMongoStorageMixin, NotebookStorage):
    def status(self, user, params, session, *args, **kwargs):
        user = UserMongo.objects(id=user.id).first()
        base = NotebookMongo.objects(Q(user=user) | Q(privacy='public'))
        return {'total': base.count(),
                'public': base.filter(NotebookMongo.level == 'public').count(),
                'private': base.filter(NotebookMongo.privacy == 'private').count()}

    def form(self):
        '''Pass through to shared method in BaseMongoStorageMixin'''
        return self._form(NotebookConfig)

    def search(self, user, params, session, *args, **kwargs):
        '''Pass through to shared method in BaseMongoStorageMixin'''
        return self._search(NotebookMongo, 'Notebook', user, params, session, *args, **kwargs)

    def list(self, user, params, session, *args, **kwargs):
        '''Pass through to shared method in BaseMongoStorageMixin'''
        return self._list(NotebookMongo, 'notebooks', user, params, session, *args, **kwargs)

    def detail(self, user, params, session, *args, **kwargs):
        '''Pass through to shared method in BaseMongoStorageMixin'''
        return self._detail(NotebookMongo, user, params, session, *args, **kwargs)

    def store(self, user, params, session, *args, **kwargs):
        name = params.get('name')
        user_sql = UserMongo.objects(user=user)

        if params.get('file') is not None:
            notebook = nbformat.writes(strip_outputs(nbformat.reads(params.get('file').file.read(), 4)))
        elif params.get('notebook'):
            notebook = nbformat.writes(strip_outputs(nbformat.reads(params.get('notebook'), 4)))
        else:
            raise NotImplementedError()

        privacy = params.get('privacy') or ''
        level = params.get('level') or ''

        if params.get('requirements') is not None:
            try:
                requirements = params.get('requirements').file.read()
            except AttributeError:
                requirements = ''
        else:
            requirements = ''

        if params.get('dockerfile'):
            try:
                params.get('dockerfile').file.read()
            except AttributeError:
                requirements = ''

        else:
            dockerfile = ''

        created = datetime.now()
        modified = datetime.now()

        id = params.get('id')
        if id:
            id = justid(id)
            nb = NotebookMongo.objects(id=id).first()
            nb.name = name
            nb.notebook = notebook
            nb.privacy = privacy
            nb.level = level
            nb.requirements = requirements
            nb.dockerfile = dockerfile
            nb.modified = modified

        else:
            nb = NotebookMongo(name=name,
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

    def delete(self, user, params, session, *args, **kwargs):
        # TODO only if allowed
        id = justid(params.get('id'))
        nb = NotebookMongo.objects(id=id).first()
        name = nb.name
        session.delete(nb)

        # cascade handled in DB, need to cascade to airflow jobs
        from .models.job import JobMongo
        jobs = JobMongo.objects(notebook=nb).all()
        for job in jobs:
            resp = self.db.jobs.delete(user, {'id': job.id}, session, *args, **kwargs)
            print(resp)
        return [{"name": "", "type": "p", "value": "Success!", "required": False, "readonly": False, "hidden": False},
                {"name": "", "type": "p", "value": "Successfully deleted notebook: " + name, "required": False, "readonly": False, "hidden": False}]
