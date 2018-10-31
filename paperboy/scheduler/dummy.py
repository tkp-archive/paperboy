# -*- coding: utf-8 -*-
import json
import os
import os.path
import jinja2
from base64 import b64encode
from random import randint, choice
from .base import BaseScheduler

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'paperboy.airflow.py')), 'r') as fp:
    TEMPLATE = fp.read()

TIMING_MAP = {
  'minutely': '*/1 * * * *',
  '5 minutes': '*/5 * * * *',
  '10 minutes': '*/10 * * * *',
  '30 minutes': '*/30 * * * *',
  'hourly': '@hourly',
  '2 hours': '0 */2 * * *',
  '3 hours': '0 */3 * * *',
  '6 hours': '0 */6 * * *',
  '12 hours': '0 */12 * * *',
  'daily': '@daily',
  'weekly': '@weekly',
  'monthly': '@monthly'
}


class DummyScheduler(BaseScheduler):
    def status(self, user, params, session, *args, **kwargs):
        type = params.get('type', '')
        if type == 'notebooks':
            return self.statusgeneral()['notebooks']
        elif type == 'jobs':
            return self.statusgeneral()['jobs']
        elif type == 'reports':
            return self.statusgeneral()['reports']
        else:
            return self.statusgeneral()

    def statusgeneral(self):
        return {'notebooks': [{'name': 'TestNB%d' % i,
                               'id': 'Notebook-%d' % i,
                               'meta': {
                                  'jobs': randint(4, 100),
                                  'done': randint(1, 4),
                                  'running': randint(1, 4),
                                  'queued': randint(1, 4),
                                  'disabled': randint(1, 4),
                                  'reports': randint(1, 1000),
                               }} for i in range(10)],
                'jobs': [{'name': 'TestJob%d' % i,
                          'id': 'Job-%d' % i,
                          'meta': {
                             'id': 'Job-1',
                             'notebookid': 'Notebook-1',
                             'reports': 353,
                             'last run': '10/14/2018 04:50:33',
                             'status': choice(['✘', '✔', '✔', '✔'])}
                          } for i in range(10)],
                'reports': [{'name': 'TestReport%d' % i,
                             'id': 'Report-%d' % i,
                             'meta': {
                                'run': '10/14/2018 04:50:33',
                                'notebookid': 'Notebook-1',
                                'jobid': 'Job-1',
                                'type': 'run',
                                'nbconvert': 'pdf',
                                'code': 'nocode',
                                'output': 'pdf'}
                             } for i in range(10)]
                }

    def schedule(self, user, notebook, job, reports, *args, **kwargs):
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
            )
        print(tpl)
        return {}
