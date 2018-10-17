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

    def status(self):
        return {'page': 1,
                'pages': 3,
                'count': 10,
                'total': 25,
                'notebooks': [
                   {'name': 'TestNB%d' % i,
                    'meta': {}
                    } for i in range(10)
                ]}

    def detail(self):
        return {'page': 1,
                'pages': 1,
                'count': 25,
                'total': 25,
                'notebooks': [
                   {'name': 'TestNB%d' % i,
                    'meta': {
                        'author': 'Test Author',
                        'visibility': choice(['public'] * 10 + ['private']),
                        'jobs': str(randint(1, 100)),
                        'reports': str(randint(1, 1000)),
                        'created': '10/14/2018 04:50:33',
                        'last modified': '10/14/2018 18:25:31'}
                    } for i in range(25)
                   ]}


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
            'options': {'type': 'label',
                        'label': 'Report options'},
            'parameters': {'type': 'file',
                           'label': 'Papermill params (.jsonl)',
                           'required': False},
            'autogen': {'type': 'checkbox',
                        'label': 'Autogenerate reports',
                        'value': 'true',
                        'required': False},
            'submit': {'type': 'submit',
                       'value': 'Create',
                       'url': urljoin(self.config.apiurl, 'jobs')}
        }

    def status(self):
        return {'page': 1,
                'pages': 15,
                'count': 10,
                'total': 150,
                'jobs': [
                        {'name': 'TestJob%d' % i,
                         'meta': {}
                         } for i in range(10)
                ]}

    def detail(self):
        return {'page': 1,
                'pages': 6,
                'count': 25,
                'total': 150,
                'jobs': [
                        {'name': 'TestJob%d' % i,
                         'meta': {
                            'notebook': 'TestNotebook',
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
                            'last run': '',
                            'status': '✘✔✔',
                            'created': '10/14/2018 04:50:33',
                            'last modified': '10/14/2018 18:25:31',
                         }
                         } for i in range(25)
                ]}


class ReportDummyStorage(ReportStorage):
    def form(self):
        return {
            'name': {'type': 'text',
                     'label': 'Name',
                     'placeholder': 'Name for Report...'},
            'notebook': {'type': 'autocomplete',
                         'label': 'Notebook',
                         'url': urljoin(self.config.apiurl, 'autocomplete?type=notebooks&partial=')},
            'job': {'type': 'autocomplete',
                    'label': 'Job',
                    'url': urljoin(self.config.apiurl, 'autocomplete?type=jobs&partial=')},
            'type': {'type': 'select',
                     'label': 'Type',
                     'options': ['Run', 'Publish']},
            'nbconvert': {'type': 'select',
                          'label': 'NBConvert',
                          'options': ['Email', 'PDF', 'HTML', 'Markdown', 'RST', 'Script']},
            'code': {'type': 'select',
                     'label': 'Strip Code',
                     'options': ['Yes', 'No']},
            'submit': {'type': 'submit',
                       'value': 'Create',
                       'url': urljoin(self.config.apiurl, 'reports')}
        }

    def status(self):
        return {'page': 1,
                'pages': 352,
                'count': 10,
                'total': 3520,
                'reports': [
                        {'name': 'TestReport%d' % i,
                         'meta': {}
                         } for i in range(10)
                ]}

    def detail(self):
        return {'page': 1,
                'pages': 141,
                'count': 25,
                'total': 3520,
                'reports': [
                        {'name': 'TestReport%d' % i,
                         'meta': {
                            'notebook': 'TestNotebook',
                            'job': 'TestJob',
                            'type': choice(['email', 'publish']),
                            'reports': str(randint(1, 1000)),
                            'created': '10/14/2018 04:50:33',
                            'last modified': '10/14/2018 18:25:31',
                             }
                         } for i in range(25)
                ]}
