# -*- coding: utf-8 -*-
import json
import os
import os.path
import jinja2
import sys
import logging
from base64 import b64encode
from ..cron import schedule_cron, unschedule_cron
from ..base import BaseScheduler, TIMING_MAP

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'paperboy.luigi.py')), 'r') as fp:
    TEMPLATE = fp.read()

LUIGI_URLS = {
    'PENDING': '/api/task_list?data={"status":"PENDING"}',
    'RUNNING': '/api/task_list?data={"status":"RUNNING"}',
    'FAILED': '/api/task_list?data={"status":"FAILED"}',
    'DONE': '/api/task_list?data={"status":"DONE"}',
    'DISABLED': '/api/task_list?data={"status":"DISABLED"}',
}


LUIGI_COMMAND = [sys.executable, '-m', 'luigi', '--module', 'MODULE', 'TAST']


class LuigiScheduler(BaseScheduler):
    def __init__(self, *args, **kwargs):
        '''Create a new airflow scheduler, connecting to the airflow instances configuration'''
        super(LuigiScheduler, self).__init__(*args, **kwargs)

    def status(self, user, params, session, *args, **kwargs):
        '''Get status of job/report tasks'''
        type = params.get('type', '')

        # TODO
        logging.debug('Scheduler offline, using fake scheduler query')
        gen = LuigiScheduler.query()
        if type == 'jobs':
            return gen.get('jobs', [])
        elif type == 'reports':
            return gen.get('reports', [])
        else:
            return gen or {}

    @staticmethod
    def query():
        '''Get status of job/report tasks from luigi'''
        return {}
        raise NotImplementedError()

    @staticmethod
    def template(config, user, notebook, job, reports, *args, **kwargs):
        '''jinja templatize airflow task for paperboy (paperboy.luigi.py)'''
        owner = user.name
        start_date = job.meta.start_time.strftime('%m/%d/%Y %H:%M:%S')
        email = 'test@test.com'
        job_json = b64encode(json.dumps(job.to_json(True)).encode('utf-8'))
        report_json = b64encode(json.dumps([r.to_json() for r in reports]).encode('utf-8'))
        interval = TIMING_MAP.get(job.meta.interval)

        tpl = jinja2.Template(TEMPLATE).render(
            owner=owner,
            start_date=start_date,
            interval=interval,
            email=email,
            job_json=job_json,
            report_json=report_json,
            output_config=json.dumps(config.output.to_json())
            )
        return tpl

    def schedule(self, user, notebook, job, reports, *args, **kwargs):
        '''Schedule a DAG for `job` omposed of `reports` to be run on airflow'''
        # create task
        template = LuigiScheduler.template(self.config, user, notebook, job, reports, *args, **kwargs)
        name = job.id + '.py'
        os.makedirs(self.config.scheduler_config.task_folder, exist_ok=True)
        with open(os.path.join(self.config.scheduler_config.task_folder, name), 'w') as fp:
            fp.write(template)

        # create crontab
        schedule_cron(self.luigi_command(os.path.join(self.config.scheduler_config.task_folder, name)), TIMING_MAP.get(job.meta.interval), self.config.scheduler_config.crontab)
        return template

    def luigi_command(self, path):
        return ' '.join((sys.executable, path))

    def unschedule(self, user, notebook, job, reports, *args, **kwargs):
        '''Remove the DAG for `user` and `notebook` composed of `job` running `reports` from
            airflow 2 parts, remove the dag from disk and delete the dag from airflow's database using the CLI'''
        if reports:
            # reschedule
            return self.schedule(user, notebook, job, reports, *args, **kwargs)

        else:
            # delete
            return unschedule_cron(self.luigi_command(os.path.join(self.config.scheduler_config.task_folder, job.id + '.py')), self.config.scheduler_config.crontab)
