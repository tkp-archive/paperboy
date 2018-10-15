from random import randint, choice


class NotebookDummyStorage(object):
    def config(self):
        return {
            'File': {'type': 'file',
                     'label': 'File'},
            'Name': {'type': 'text',
                     'label': 'Name',
                     'placeholder': 'Name for Notebook...'},
            'Privacy': {'type': 'select',
                        'label': 'Visibility',
                        'options': ['Private', 'Public']},
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
                     'placeholder': 'Name for Job...'},
            'Notebook': {'type': 'autocomplete',
                         'label': 'Notebook',
                         'url': '/api/v1/autocomplete?type=notebooks&partial='},
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
