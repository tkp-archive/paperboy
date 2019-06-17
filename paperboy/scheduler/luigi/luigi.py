# -*- coding: utf-8 -*-
import json
import os
import os.path
import jinja2
import subprocess
import logging
from base64 import b64encode
from random import choice
from ..base import BaseScheduler, TIMING_MAP

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'paperboy.luigi.py')), 'r') as fp:
    TEMPLATE = fp.read()


class LuigiScheduler(BaseScheduler):
    def __init__(self, *args, **kwargs):
        '''Create a new airflow scheduler, connecting to the airflow instances configuration'''
        super(LuigiScheduler, self).__init__(*args, **kwargs)

    def status(self, user, params, session, *args, **kwargs):
        '''Get status of job/report tasks'''
        type = params.get('type', '')

        # TODO
        logging.debug('Scheduler offline, using fake scheduler query')
        gen = LuigiScheduler.fakequery()
        if type == 'jobs':
            return gen['jobs']
        elif type == 'reports':
            return gen['reports']
        else:
            return gen

    @staticmethod
    def query(engine):
        '''Get status of job/report tasks from luigi'''
        raise NotImplementedError()

    @staticmethod
    def fakequery():
        '''If luigi not present, fake the results for now so the UI looks ok'''
        ret = {'jobs': [], 'reports': []}
        for i in range(10):
            ret['jobs'].append(
                {'name': 'JobTask-{}'.format(i),
                 'id': 'JobTask-{}'.format(i),
                 'meta': {
                    'id':  'JobTask-{}'.format(i),
                    'execution': '01/02/2018 12:25:31',
                    'status': choice(['✔', '✘'])}
                 }
            )
            ret['reports'].append(
                {'name': 'ReportTask-{}'.format(i),
                 'id': 'ReportTask-{}'.format(i),
                 'meta': {
                    'run': '01/02/2018 12:25:31',
                    'status': choice(['✔', '✘']),
                    'type': choice(['Post', 'Papermill', 'NBConvert', 'Setup']),
                    }
                 }
            )
        return ret

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
        '''Schedule a DAG for `job` composed of `reports` to be run on airflow'''
        template = AirflowScheduler.template(self.config, user, notebook, job, reports, *args, **kwargs)
        name = job.id + '.py'
        os.makedirs(self.config.scheduler.dagbag, exist_ok=True)
        with open(os.path.join(self.config.scheduler.dagbag, name), 'w') as fp:
            fp.write(template)
        return template

    def unschedule(self, user, notebook, job, reports, *args, **kwargs):
        '''Remove the DAG for `user` and `notebook` composed of `job` running `reports` from
            airflow 2 parts, remove the dag from disk and delete the dag from airflow's database using the CLI'''
        if reports:
            # reschedule
            return self.schedule(user, notebook, job, reports, *args, **kwargs)

        else:
            # delete
            name = job.id + '.py'
            file = os.path.join(self.config.scheduler.dagbag, name)
            dag = 'DAG-' + job.id

            # delete dag file
            os.remove(file)

            # delete dag
            # FIXME
            try:
                cmd = ['airflow', 'delete_dag', dag, '-y']
                subprocess.call(cmd)
            except Exception as e:
                print(e)
