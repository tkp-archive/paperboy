import json
import nbformat
from random import randint, choice
from six.moves.urllib_parse import urljoin
from .base import NotebookStorage, JobStorage, ReportStorage


class NotebookDummyStorage(NotebookStorage):
    def form(self):
        return {
            'file': {'type': 'file',
                     'label': 'File',
                     'required': True},
            'name': {'type': 'text',
                     'label': 'Name',
                     'placeholder': 'Name for Notebook...',
                     'required': True},
            'privacy': {'type': 'select',
                        'label': 'Visibility',
                        'options': ['Private', 'Public'],
                        'required': True},
            'build': {'type': 'label',
                      'label': 'Build options'},
            'requirements': {'type': 'file',
                             'label': 'requirements.txt',
                             'required': False},
            'dockerfile': {'type': 'file',
                           'label': 'Dockerfile',
                           'required': False},
            'submit': {'type': 'submit',
                       'value': 'Create',
                       'url': urljoin(self.config.apiurl, 'notebooks')}
        }

    def list(self):
        return {'page': 1,
                'pages': 1,
                'count': 25,
                'total': 25,
                'notebooks': [
                   {'name': 'TestNB%d' % i,
                    'id': 'Notebook-%d' % i,
                    'meta': {
                        'author': 'Test Author',
                        'visibility': choice(['public'] * 10 + ['private']),
                        'jobs': str(randint(1, 100)),
                        'reports': str(randint(1, 1000)),
                        'created': '10/14/2018 04:50:33',
                        'last modified': '10/14/2018 18:25:31'}
                    } for i in range(25)
                   ]}

    def detail(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({
            'name': 'MyNotebook',
            'id': 'Notebook-1',
            'author': 'Joe Python',
            'jobs': 25,
            'reports': 353,
            'created': '10/14/2018 04:50:33',
            'last modified': '10/14/2018 18:25:31',
        })

    def store(self, req, resp):
        name = req.get_param('name')
        nb = nbformat.reads(req.get_param('file').file.read(), 4)
        resp.content_type = 'application/json'
        resp.body = json.dumps([
            {'type': 'h2',
             'content': 'Success!'},
            {'type': 'p',
             'content': 'Successfully stored notebook {}'.format(name)}
        ])


class JobDummyStorage(JobStorage):
    def form(self):
        return {
            'name': {'type': 'text',
                     'label': 'Name',
                     'placeholder': 'Name for Job...',
                     'required': True},
            'notebook': {'type': 'autocomplete',
                         'label': 'Notebook',
                         'url': urljoin(self.config.apiurl, 'autocomplete?type=notebooks&partial='),
                         'required': True},
            'starttime': {'type': 'datetime',
                          'label': 'Start Time/Date',
                          'required': True},
            'interval': {'type': 'select',
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
            'parameters_inline': {'type': 'textarea',
                                  'label': 'Papermill params (.jsonl)',
                                  'placeholder': 'Upload file or type here...',
                                  'required': False},
            'parameters': {'type': 'file',
                           'label': 'Papermill params (.jsonl)',
                           'required': False},
            'options': {'type': 'label',
                        'label': 'Report options'},
            'type': {'type': 'select',
                     'label': 'Type',
                     'options': ['Run', 'Publish'],
                     'required': True},
            'nbconvert': {'type': 'select',
                          'label': 'NBConvert',
                          'options': ['Email', 'PDF', 'HTML', 'Markdown', 'RST', 'Script'],
                          'required': True},
            'code': {'type': 'select',
                     'label': 'Strip Code',
                     'options': ['Yes', 'No'],
                     'required': True},
            'autogen': {'type': 'checkbox',
                        'label': 'Autogenerate reports',
                        'value': 'true',
                        'required': False},
            'submit': {'type': 'submit',
                       'value': 'Create',
                       'url': urljoin(self.config.apiurl, 'jobs')}
        }

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
        resp.body = json.dumps({
            'name': 'MyJob',
            'id': 'Job-1',
            'author': 'Joe Python',
            'notebook': 'MyNotebook',
            'notebookid': 'Notebook-1',
            'reports': 353,
            'type': 'run',
            'nbconvert': 'email',
            'code': 'nocode',
            'created': '10/14/2018 04:50:33',
            'last modified': '10/14/2018 18:25:31',
        })

    def store(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({
            'name': 'MyJob',
            'author': 'Joe Python',
            'notebook': 'MyNotebook1',
            'reports': 253,
            'last run': '10/14/2018 04:50:33',
        })


class ReportDummyStorage(ReportStorage):
    def form(self):
        return {
            'name': {'type': 'text',
                     'label': 'Name',
                     'placeholder': 'Name for Report...',
                     'required': True},
            'notebook': {'type': 'autocomplete',
                         'label': 'Notebook',
                         'url': urljoin(self.config.apiurl, 'autocomplete?type=notebooks&partial='),
                         'required': True},
            'job': {'type': 'autocomplete',
                    'label': 'Job',
                    'url': urljoin(self.config.apiurl, 'autocomplete?type=jobs&partial='),
                    'required': True},
            'params': {'type': 'textarea',
                       'label': 'Parameters',
                       'placeholder': 'JSON Parameters...'},
            'type': {'type': 'select',
                     'label': 'Type',
                     'options': ['Run', 'Publish'],
                     'required': True},
            'nbconvert': {'type': 'select',
                          'label': 'NBConvert',
                          'options': ['Email', 'PDF', 'HTML', 'Markdown', 'RST', 'Script'],
                          'required': True},
            'code': {'type': 'select',
                     'label': 'Strip Code',
                     'options': ['Yes', 'No'],
                     'required': True},
            'submit': {'type': 'submit',
                       'value': 'Create',
                       'url': urljoin(self.config.apiurl, 'reports')}
        }

    def list(self):
        return {'page': 1,
                'pages': 141,
                'count': 25,
                'total': 3520,
                'reports': [
                        {'name': 'TestReport%d' % i,
                         'id': 'Report-%d' % i,
                         'meta': {
                            'notebook': 'TestNotebook',
                            'notebookid': 'Notebook-%d' % i,
                            'job': 'TestJob',
                            'notebookid': 'Job-%d' % i,
                            'type': choice(['email', 'publish']),
                            'reports': str(randint(1, 1000)),
                            'created': '10/14/2018 04:50:33',
                            'last modified': '10/14/2018 18:25:31',
                             }
                         } for i in range(25)
                ]}

    def detail(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({
            'name': 'MyReport',
            'id': 'Report-1',
            'author': 'Joe Python',
            'notebook': 'MyNotebook1',
            'notebookid': 'Notebook-1',
            'job': 'MyJob1',
            'jobid': 'Job-1',
            'type': 'run',
            'nbconvert': 'pdf',
            'code': 'nocode',
            'output': 'pdf',
            'run date': '10/14/2018 04:50:33'
        })

    def store(self, req, resp):
        name = req.get_param('name')
        nb_name = req.get_param('notebook')
        rp_name = req.get_param('report')
        resp.content_type = 'application/json'
        resp.body = json.dumps([
            {'type': 'h2',
             'content': 'Success!'},
            {'type': 'p',
             'content': 'Successfully configured report {}'.format(name)},
            {'type': 'p',
             'content': 'Notebook: {}'.format(nb_name)},
            {'type': 'p',
             'content': 'Report: {}'.format(rp_name)}])
