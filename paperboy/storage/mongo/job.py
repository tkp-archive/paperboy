import logging
from datetime import datetime
from paperboy.config import JobConfig
from paperboy.storage import JobStorage
from .base import BaseMongoStorageMixin, justid
from .models.user import UserMongo
from .models.notebook import NotebookMongo
from .models.job import JobMongo


class JobMongoStorage(BaseMongoStorageMixin, JobStorage):
    def status(self, user, params, session, *args, **kwargs):
        user = UserMongo.objects(id=user.id).first()
        base = JobMongo.objects(user=user)
        return {'total': base.count(),
                'production': base.filter(JobMongo.level == 'production').count(),
                'research': base.filter(JobMongo.level == 'research').count(),
                'development': base.filter(JobMongo.level == 'development').count(),
                'personal': base.filter(JobMongo.level == 'personal').count()}

    def form(self):
        '''Pass through to shared method in BaseMongoStorageMixin'''
        return self._form(JobConfig)

    def search(self, user, params, session, *args, **kwargs):
        '''Pass through to shared method in BaseMongoStorageMixin'''
        return self._search(JobMongo, 'Job', user, params, session, *args, **kwargs)

    def list(self, user, params, session, *args, **kwargs):
        '''Pass through to shared method in BaseMongoStorageMixin'''
        return self._list(JobMongo, 'jobs', user, params, session, *args, **kwargs)

    def detail(self, user, params, session, *args, **kwargs):
        '''Pass through to shared method in BaseMongoStorageMixin'''
        return self._detail(JobMongo, user, params, session, *args, **kwargs)

    def store(self, user, params, session, scheduler, *args, **kwargs):
        name = params.get('name')
        user_sql = session.query(UserMongo).get(int(user.id))
        notebookid = params.get('notebook')
        nb_sql = session.query(NotebookMongo).get(int(justid(notebookid)))
        notebook_config = nb_sql.to_config(self.config)

        start_time = datetime.strptime(params.get('starttime'), '%Y-%m-%dT%H:%M')
        interval = params.get('interval') or ''
        level = params.get('level') or ''
        created = datetime.now()
        modified = datetime.now()

        id = params.get('id')
        if id:
            id = justid(id)
            jb = session.query(JobMongo).filter(JobMongo.id == id).first()
            jb.name = name
            jb.start_time = start_time
            jb.interval = interval
            jb.level = level
            jb.modified = modified

        else:
            jb = JobMongo(name=name,
                          userId=user.id,
                          user=user_sql,
                          notebookId=notebookid,
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
        job_config = jb.to_config(self.config)
        store = job_config.store()

        # autogenerate reports
        report_configs = self.db.reports.generate(user, params, session, job=job_config, *args, **kwargs)
        if report_configs:
            # reload to get accurate report count
            session.flush()
            session.refresh(jb)
            job_config = jb.to_config(self.config)
            store = job_config.store()

        scheduler.schedule(user, notebook_config, job_config, report_configs)
        return store

    def delete(self, user, params, session, scheduler, *args, **kwargs):
        # TODO only if allowed
        id = justid(params.get('id'))
        jb = session.query(JobMongo).filter(JobMongo.id == id).first()
        name = jb.name
        session.delete(jb)

        scheduler.unschedule(user, None, jb.to_config(self.config), [])

        return [{"name": "", "type": "p", "value": "Success!", "required": False, "readonly": False, "hidden": False},
                {"name": "", "type": "p", "value": "Successfully deleted job: " + name, "required": False, "readonly": False, "hidden": False}]
