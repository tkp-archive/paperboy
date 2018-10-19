import json
from random import randint, choice
from six.moves.urllib_parse import urljoin

from paperboy.config import Job
from ..base import JobStorage


class JobDummyStorage(JobStorage):
    def object(self):
        return Job

    def form(self):
        return [
            {'name': 'name',
             'type': 'text',
             'label': 'Name',
             'placeholder': 'Name for Job...',
             'required': True},
            {'name': 'notebook',
             'type': 'autocomplete',
             'label': 'Notebook',
             'url': urljoin(self.config.apiurl, 'autocomplete?type=notebooks&partial='),
             'required': True},
            {'name': 'starttime',
             'type': 'datetime',
             'label': 'Start Time/Date',
             'required': True},
            {'name': 'interval',
             'type': 'select',
             'label': 'Interval',
             'options': ['minutely',
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
                         'monthly'],
             'required': True},
            {'name': 'parameters_inline',
             'type': 'textarea',
             'label': 'Papermill params (.jsonl)',
             'placeholder': 'Upload file or type here...',
             'required': False},
            {'name': 'parameters',
             'type': 'file',
             'label': 'Papermill params (.jsonl)',
             'required': False},
            {'name': 'options',
             'type': 'label',
             'label': 'Report options'},
            {'name': 'name',
             'type': 'select',
             'label': 'Type',
             'options': ['Run', 'Publish'],
             'required': True},
            {'name': 'output',
             'type': 'select',
             'label': 'Output',
             'options': ['Email', 'PDF', 'HTML', 'Script'],
             'required': True},
            {'name': 'code',
             'type': 'select',
             'label': 'Strip Code',
             'options': ['Yes', 'No'],
             'required': True},
            {'name': 'autogen',
             'type': 'checkbox',
             'label': 'Autogenerate reports',
             'value': 'true',
             'required': False},
            {'name': 'submit',
             'type': 'submit',
             'value': 'Create',
             'url': urljoin(self.config.apiurl, 'jobs')}
        ]

    def list(self):
        return {'page': 1,
                'pages': 6,
                'count': 25,
                'total': 150,
                'jobs': [
                        {'name': 'TestJob%d' % i,
                         'id': 'Job-%d' % i,
                         'meta': {
                            'notebook': 'TestNotebook',
                            'notebookid': 'Notebook-%d' % i,
                            'owner': 'TestOwner',
                            'reports': str(randint(1, 1000)),
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
                            'last modified': '10/14/2018 18:25:31',
                         }
                         } for i in range(25)
                ]}

    def detail(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps([
            {'name': 'name',
             'type': 'text',
             'value': 'MyJob',
             'required': True},
            {'name': 'id',
             'type': 'text',
             'value': 'Job-1',
             'required': True,
             'readonly': True},
            {'name': 'author',
             'type': 'text',
             'value':  'Joe Python',
             'required': True,
             'readonly': True},
            {'name': 'notebook',
             'type': 'autocomplete',
             'value':  'MyNotebook',
             'required': True,
             'readonly': True},
            {'name': 'reports',
             'type': 'text',
             'value':  '353',
             'readonly': True},
            {'name': 'type',
             'type': 'select',
             'options':  ['run']},
            {'name': 'output',
             'type': 'select',
             'options':  ['email']},
            {'name': 'code',
             'type': 'select',
             'options':  ['nocode']},
            {'name': 'created',
             'type': 'datetime',
             'value':  '10/14/2018 04:50:33',
             'readonly': True},
            {'name': 'last modified',
             'type': 'datetime',
             'value': '10/14/2018 18:25:31',
             'readonly': True},
            {'name': 'save',
             'type': 'submit',
             'value': 'Save',
             'url': urljoin(self.config.apiurl, 'notebooks')}
        ])

    def store(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({
            'name': 'MyJob',
            'author': 'Joe Python',
            'notebook': 'MyNotebook1',
            'reports': 253,
            'last run': '10/14/2018 04:50:33',
        })
