import json
from random import choice, randint
from .base import BaseScheduler


class DummyScheduler(BaseScheduler):
    def status(self, req, resp):
        resp.content_type = 'application/json'
        type = req.params.get('type', '')
        if type == 'notebooks':
            resp.body = json.dumps(self.statusnb())
        elif type == 'jobs':
            resp.body = json.dumps(self.statusjb())
        elif type == 'reports':
            resp.body = json.dumps(self.statusrp())
        else:
            resp.body = json.dumps(self.statusgeneral())

    def statusnb(self):
        return [{'name': 'TestNB%d' % i,
                 'id': 'Notebook-%d' % i,
                 'meta': {
                    'jobs': randint(4, 100),
                    'running': choice([1, 2, 3]),
                    'reports': randint(1, 1000),
                 }
                 } for i in range(10)]

    def statusjb(self):
        return [{'name': 'TestJob%d' % i,
                 'id': 'Job-%d' % i,
                 'meta': {
                    'id': 'Job-1',
                    'notebookid': 'Notebook-1',
                    'reports': 353,
                    'last run': '10/14/2018 04:50:33',
                    'status': choice(['✘', '✔', '✔', '✔'])}
                 } for i in range(10)]

    def statusrp(self):
        return [{'name': 'TestReport%d' % i,
                 'id': 'Report-%d' % i,
                 'meta': {
                    'run': '10/14/2018 04:50:33',
                    'notebook': 'MyNotebook1',
                    'notebookid': 'Notebook-1',
                    'job': 'MyJob1',
                    'jobid': 'Job-1',
                    'type': 'run',
                    'nbconvert': 'pdf',
                    'code': 'nocode',
                    'output': 'pdf'}
                 } for i in range(10)]

    def statusgeneral(self):
        return {'notebooks': {
                    'total': 25,
                    'production': 15,
                    'research': 3,
                    'mine': 7},
                'jobs': {
                    'total': 150,
                    'done': 25,
                    'running': 10,
                    'queue': 60,
                    'disabled': 55},
                'reports': {
                    'total': 3250,
                    'published': 2074,
                    'unpublished': 276,
                    'public': 2755,
                    'private': 495}}
