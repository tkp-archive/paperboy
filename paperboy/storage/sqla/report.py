import os
import json
import logging
from datetime import datetime
from paperboy.config import Report
from paperboy.config.storage import ReportListResult
from paperboy.storage import ReportStorage
from .base import BaseSQLStorageMixin, justid
from .models.user import UserSQL
from .models.notebook import NotebookSQL
from .models.job import JobSQL
from .models.report import ReportSQL


class ReportSQLStorage(BaseSQLStorageMixin, ReportStorage):
    def status(self, session, *args, **kwargs):
        return {'total': session.query(ReportSQL).count(),
                'notebook': session.query(ReportSQL).filter(ReportSQL.output == 'notebook').count(),
                'pdf': session.query(ReportSQL).filter(ReportSQL.output == 'pdf').count(),
                'html': session.query(ReportSQL).filter(ReportSQL.output == 'html').count(),
                'email': session.query(ReportSQL).filter(ReportSQL.output == 'email').count(),
                'script': session.query(ReportSQL).filter(ReportSQL.output == 'script').count()}

    def form(self):
        return self._form(Report)

    def search(self, count, id=None, name=None, session=None, *args, **kwargs):
        return self._search(ReportSQL, 'Report', count, id, name, session, *args, **kwargs)

    def list(self, req, resp, session, *args, **kwargs):
        return self._list(ReportSQL, ReportListResult, 'reports', req, resp, session, *args, **kwargs)

    def detail(self, req, resp, session, *args, **kwargs):
        return self._detail(ReportSQL, req, resp, session, *args, **kwargs)

    def store(self, req, resp, session, *args, **kwargs):
        name = req.get_param('name')

        user = req.context['user']
        user_sql = session.query(UserSQL).get(int(user.id))

        notebook = req.get_param('notebook')
        nb_sql = session.query(NotebookSQL).get(int(justid(notebook)))

        job = req.get_param('job')
        jb_sql = session.query(JobSQL).get(int(justid(job)))

        type = req.get_param('type') or 'run'
        output = req.get_param('output') or 'pdf'
        strip_code = req.get_param('strip_code') == 'yes'
        parameters = req.get_param('parameters') or '[]'

        created = datetime.now()
        modified = datetime.now()

        rp = ReportSQL(name=name,
                       userId=user.id,
                       user=user_sql,
                       notebookId=notebook,
                       notebook=nb_sql,
                       jobId=job,
                       job=jb_sql,
                       type=type,
                       output=output,
                       strip_code=strip_code,
                       parameters=parameters,
                       created=created,
                       modified=modified)
        session.add(rp)

        # generate id
        session.flush()
        session.refresh(rp)

        resp.content_type = 'application/json'
        store = rp.to_config(self.config).store()
        logging.critical("Storing report {}".format(rp))
        resp.body = json.dumps(store)

    def generate(self, req, resp, session, *args, **kwargs):
        autogen = req.get_param('autogen') or False
        if autogen:
            parameters_inline = req.get_param('parameters_inline') or ''
            parameters = req.get_param('parameters')
            if not parameters_inline and parameters:
                params = parameters.file.read()
            else:
                params = parameters_inline
            params = params.split(os.linesep)
            params = [json.loads(p) for p in params]

            user = req.context['user']
            user_sql = session.query(UserSQL).get(int(user.id))

            notebook = req.get_param('notebook')
            nb_sql = session.query(NotebookSQL).get(int(justid(notebook)))

            job_name = req.get_param('name')
            job_id = kwargs.get('jobid')
            jb_sql = session.query(JobSQL).get(int(justid(job_id)))

            type = req.get_param('type') or 'run'
            output = req.get_param('output') or 'notebook'
            strip_code = req.get_param('code') or 'no'

            created = datetime.now()
            modified = datetime.now()

            for i, param in enumerate(params):
                name = job_name + '-Report-' + str(i)
                param = json.dumps(param)
                rp = ReportSQL(name=name,
                               userId=user.id,
                               user=user_sql,
                               notebookId=notebook,
                               notebook=nb_sql,
                               jobId=job_id,
                               job=jb_sql,
                               type=type,
                               output=output,
                               strip_code=strip_code,
                               parameters=param,
                               created=created,
                               modified=modified)
                session.add(rp)
            session.flush()

            return len(params)
        return False
