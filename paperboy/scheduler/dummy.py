import json
from random import randint, choice
from .base import BaseScheduler


class DummyScheduler(BaseScheduler):
    def status(self, req, resp, *args, **kwargs):
        resp.content_type = 'application/json'
        type = req.params.get('type', '')
        if type == 'notebooks':
            resp.body = json.dumps(self.statusgeneral()['notebooks'])
        elif type == 'jobs':
            resp.body = json.dumps(self.statusgeneral()['jobs'])
        elif type == 'reports':
            resp.body = json.dumps(self.statusgeneral()['reports'])
        else:
            resp.body = json.dumps(self.statusgeneral())

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
