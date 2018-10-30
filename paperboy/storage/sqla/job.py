import logging
from datetime import datetime
from paperboy.config import Job
from paperboy.config.storage import JobListResult
from paperboy.storage import JobStorage
from .base import BaseSQLStorageMixin, justid
from .models.user import UserSQL
from .models.notebook import NotebookSQL
from .models.job import JobSQL


class JobSQLStorage(BaseSQLStorageMixin, JobStorage):
    def status(self, session, *args, **kwargs):
        return {'total': session.query(JobSQL).count(),
                'production': session.query(JobSQL).filter(JobSQL.level == 'production').count(),
                'research': session.query(JobSQL).filter(JobSQL.level == 'research').count(),
                'development': session.query(JobSQL).filter(JobSQL.level == 'development').count(),
                'personal': session.query(JobSQL).filter(JobSQL.level == 'personal').count()}

    def form(self):
        return self._form(Job)

    def search(self, user, params, session, *args, **kwargs):
        return self._search(JobSQL, 'Job', user, params, session, *args, **kwargs)

    def list(self, user, params, session, *args, **kwargs):
        return self._list(JobSQL, JobListResult, 'jobs', user, params, session, *args, **kwargs)

    def detail(self, user, params, session, *args, **kwargs):
        return self._detail(JobSQL, user, params, session, *args, **kwargs)

    def store(self, user, params, session, *args, **kwargs):
        name = params.get('name')
        user_sql = session.query(UserSQL).get(int(user.id))
        notebook = params.get('notebook')
        nb_sql = session.query(NotebookSQL).get(int(justid(notebook)))

        start_time = datetime.strptime(params.get('starttime'), '%Y-%m-%dT%H:%M')
        interval = params.get('interval') or ''
        level = params.get('level') or ''
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
        reports_created = self.db.reports.generate(user, params, session, jobid=jb.id, *args, **kwargs)
        if reports_created:
            # reload to get accurate report count
            session.flush()
            session.refresh(jb)
            store = jb.to_config(self.config).store()

        return store
