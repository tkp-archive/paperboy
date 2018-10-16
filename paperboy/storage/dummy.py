from random import randint, choice


class NotebookDummyStorage(object):
    def config(self):
        return {
            'File': {'type': 'file',
                     'label': 'File',
                     'required': True},
            'Name': {'type': 'text',
                     'label': 'Name',
                     'placeholder': 'Name for Notebook...',
                     'required': True},
            'Privacy': {'type': 'select',
                        'label': 'Visibility',
                        'options': ['Private', 'Public'],
                        'required': True},
            'Requirements': {'type': 'file',
                             'label': 'requirements.txt',
                             'required': False},
            'Dockerfile': {'type': 'file',
                           'label': 'Dockerfile',
                           'required': False},
            'Submit': {'type': 'submit',
                       'value': 'Create',
                       'url': 'test'}
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


class JobDummyStorage(object):
    def config(self):
        return {
            'Name': {'type': 'text',
                     'label': 'Name',
                     'placeholder': 'Name for Job...',
                     'required': True},
            'Notebook': {'type': 'autocomplete',
                         'label': 'Notebook',
                         'url': '/api/v1/autocomplete?type=notebooks&partial=',
                         'required': True},
            'Starttime': {'type': 'datetime',
                          'label': 'Start Time/Date',
                          'required': True},
            'Interval': {'type': 'select',
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
            'Submit': {'type': 'submit',
                       'value': 'Create',
                       'url': 'test'}
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
                            'created': '10/14/2018 04:50:33',
                            'last modified': '10/14/2018 18:25:31',
                         }
                         } for i in range(25)
                ]}


class ReportDummyStorage(object):
    def config(self):
        return {
            'Name': {'type': 'text',
                     'label': 'Name',
                     'placeholder': 'Name for Report...'},
            'Notebook': {'type': 'autocomplete',
                         'label': 'Notebook',
                         'url': '/api/v1/autocomplete?type=notebooks&partial='},
            'Job': {'type': 'autocomplete',
                    'label': 'Job',
                    'url': '/api/v1/autocomplete?type=jobs&partial='},
            'Type': {'type': 'select',
                     'label': 'Type',
                     'options': ['Email', 'PDF', 'HTML']},
            'Submit': {'type': 'submit',
                       'value': 'Create',
                       'url': 'test'}
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
