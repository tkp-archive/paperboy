import json
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
        reports_created = self.db.reports.generate(req, resp, session, jobid=jb.id, *args, **kwargs)
        if reports_created:
            # reload to get accurate report count
            session.flush()
            session.refresh(jb)
            store = jb.to_config(self.config).store()

        resp.content_type = 'application/json'
        resp.body = json.dumps(store)
