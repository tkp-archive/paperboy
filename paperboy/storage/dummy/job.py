import json
import logging
from random import randint, choice
from paperboy.config import Job
from paperboy.config.storage import JobListResult
from paperboy.storage import JobStorage


class JobDummyStorage(JobStorage):
    def status(self, *args, **kwargs):
        return {
                    'total': 150,
                    'done': 25,
                    'running': 10,
                    'queued': 60,
                    'disabled': 55}

    def form(self):
        return Job(self.config).form()

    def search(self, count, id=None, name=None, session=None, *args, **kwargs):
        return [{'id': i, 'name': 'TestJob{}'.format(i)} for i in range(20)]

    def list(self, req, resp, *args, **kwargs):
        resp.content_type = 'application/json'
        result = JobListResult()
        result.page = 1
        result.pages = 141
        result.count = 25
        result.total = 3520
        result.jobs = [
                    Job.from_json({'name': 'TestJob%d' % i,
                                   'id': 'Job-%d' % i,
                                   'meta': {
                                      # 'notebook': 'TestNotebook',
                                      # 'notebookid': 'Notebook-%d' % i,
                                      'username': 'TestOwner',
                                      'userid': '1',
                                      'reports': randint(1, 1000),
                                      'interval': choice(['minutely',
                                                          '5 minutes',
                                                          '10 minutes',
                                                          '30 minutes',
                                                          'hourly',
                                                          '2 hours',
                                                          '3 hours',
                                                          '6 hours',
                                                          '12 hours',
                                                          'daily',
                                                          'weekly',
                                                          'monthly']),
                                      'created': '10/14/2018 04:50:33',
                                      'modified': '10/14/2018 18:25:31',
                                       }
                                   }, self.config) for i in range(25)
                ]
        resp.body = json.dumps(result.to_json())

    def detail(self, req, resp, *args, **kwargs):
        resp.content_type = 'application/json'
        store = Job.from_json(
                        {'name': 'TestJob1',
                         'id': 'Job-1',
                         'meta': {
                            # 'notebook': 'TestNotebook',
                            # 'notebookid': 'Notebook-%d' % i,
                            'username': 'TestOwner',
                            'userid': '1',
                            'reports': randint(1, 1000),
                            'interval': choice(['minutely',
                                                '5 minutes',
                                                '10 minutes',
                                                '30 minutes',
                                                'hourly',
                                                '2 hours',
                                                '3 hours',
                                                '6 hours',
                                                '12 hours',
                                                'daily',
                                                'weekly',
                                                'monthly']),
                            'created': '10/14/2018 04:50:33',
                            'modified': '10/14/2018 18:25:31'}},
                        self.config).edit()
        resp.body = json.dumps(store)

    def store(self, req, resp, *args, **kwargs):
        name = req.get_param('name')
        nb_name = req.get_param('notebook')
        resp.content_type = 'application/json'
        store = Job.from_json(
                        {'name': 'TestJob1',
                         'id': 'Job-1',
                         'meta': {
                            # 'notebook': 'TestNotebook',
                            # 'notebookid': 'Notebook-%d' % i,
                            'username': 'TestOwner',
                            'userid': '1',
                            'reports': randint(1, 1000),
                            'interval': choice(['minutely',
                                                '5 minutes',
                                                '10 minutes',
                                                '30 minutes',
                                                'hourly',
                                                '2 hours',
                                                '3 hours',
                                                '6 hours',
                                                '12 hours',
                                                'daily',
                                                'weekly',
                                                'monthly']),
                            'created': '10/14/2018 04:50:33',
                            'modified': '10/14/2018 18:25:31',
                             }},
                        self.config).store()
        logging.critical("Storing job {}".format(name))
        resp.body = json.dumps(store)
