# -*- coding: utf-8 -*-
import configparser
import json
import os
import os.path
import jinja2
from sqlalchemy import create_engine
from base64 import b64encode
from random import randint, choice
from .base import BaseScheduler, TIMING_MAP

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'paperboy.airflow.py')), 'r') as fp:
    TEMPLATE = fp.read()

QUERY = '''
SELECT task_id, dag_id, execution_date, state, unixname
FROM task_instance
ORDER BY execution_date ASC
LIMIT 20;
'''


class DummyScheduler(BaseScheduler):
    def __init__(self, *args, **kwargs):
        super(DummyScheduler, self).__init__(*args, **kwargs)
        cp = configparser.ConfigParser()
        cp.read(self.config.scheduler.config)
        try:
            self.sql_conn = cp['core']['sql_alchemy_conn']
        except KeyError:
            self.sql_conn = ''

        if self.sql_conn:
            self.engine = create_engine(self.sql_conn)

    def status(self, user, params, session, *args, **kwargs):
        type = params.get('type', '')
        if not self.sql_conn:
            if type == 'jobs':
                return self.statusgeneralfake()['jobs']
            elif type == 'reports':
                return self.statusgeneralfake()['reports']
            else:
                return self.statusgeneralfake()
        if type == 'jobs':
            return self.statusgeneral()['jobs']
        elif type == 'reports':
            return self.statusgeneral()['reports']
        else:
            return self.statusgeneral()

    def statusgeneral(self):
        ret = {'jobs': [], 'reports': []}
        with self.engine.begin() as conn:
            res = conn.execute(QUERY)
            for i, item in enumerate(res):
                ret['jobs'].append(
                    {'name': item[1],
                     'id': item[1][4:],
                     'meta': {
                        'id':  item[1][4:],
                        'execution': item[2].strftime('%m/%d/%Y %H:%M:%S'),
                        'status': '✔' if item[3] == 'success' else '✘'}
                     }
                )

                report_name = item[0].replace('ReportPost-', '') \
                                     .replace('Report-', '') \
                                     .replace('ReportNBConvert-', '') \
                                     .replace('ReportPapermill-', '')

                report_type = 'Post' if 'ReportPost' in item[0] else \
                              'Papermill' if 'Papermill' in item[0] else \
                              'NBConvert' if 'NBConvert' in item[0] else \
                              'Setup'

                ret['reports'].append(
                    {'name': item[0],
                     'id': report_name,
                     'meta': {
                        'run': item[2].strftime('%m/%d/%Y %H:%M:%S'),
                        'status': '✔' if item[3] == 'success' else '✘',
                        'type': report_type
                        }
                     }
                )
            return ret

    def statusgeneralfake(self):
        ret = {'jobs': [], 'reports': []}
        for i in range(10):
            ret['jobs'].append(
                {'name': 'DAG-Job-{}'.format(i),
                 'id': 'Job-{}'.format(i),
                 'meta': {
                    'id':  'Job-{}'.format(i),
                    'execution': '01/02/2018 12:25:31',
                    'status': choice(['✔', '✘'])}
                 }
            )
            ret['reports'].append(
                {'name': 'Report-{}'.format(i),
                 'id': 'Report-{}'.format(i),
                 'meta': {
                    'run': '01/02/2018 12:25:31',
                    'status': choice(['✔', '✘']),
                    'type': choice(['Post', 'Papermill', 'NBConvert', 'Setup']),
                    }
                 }
            )
            return ret

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
            output_config=json.dumps(self.config.output.to_json())
            )
        with open(os.path.join(self.config.scheduler.dagbag, job.id + '.py'), 'w') as fp:
            fp.write(tpl)
        return tpl
