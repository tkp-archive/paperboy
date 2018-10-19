import json
from random import randint, choice
from six.moves.urllib_parse import urljoin
from paperboy.config import Report
from ..base import ReportStorage


class ReportDummyStorage(ReportStorage):
    def object(self):
        return Report

    def form(self):
        return [
            {'name': 'name',
             'type': 'text',
             'label': 'Name',
             'placeholder': 'Name for Report...',
             'required': True},
            {'name': 'notebook',
             'type': 'autocomplete',
             'label': 'Notebook',
             'url': urljoin(self.config.apiurl, 'autocomplete?type=notebooks&partial='),
             'required': True},
            {'name': 'job',
             'type': 'autocomplete',
             'label': 'Job',
             'url': urljoin(self.config.apiurl, 'autocomplete?type=jobs&partial='),
             'required': True},
            {'name': 'params',
             'type': 'textarea',
             'label': 'Parameters',
             'placeholder': 'JSON Parameters...'},
            {'name': 'type',
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
            {'name': 'submit',
             'type': 'submit',
             'value': 'Create',
             'url': urljoin(self.config.apiurl, 'reports')}
        ]

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
                            'jobid': 'Job-%d' % i,
                            'type': choice(['email', 'publish']),
                            'reports': str(randint(1, 1000)),
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
             'value': 'MyReport',
             'required': True},
            {'name': 'id',
             'type': 'text',
             'value': 'Report-1',
             'required': True,
             'readonly': True},
            {'name': 'author',
             'type': 'text',
             'value':  'Joe Python',
             'required': True,
             'readonly': True},
            {'name': 'notebook',
             'type': 'text',
             'value':  'MyNotebook',
             'required': True,
             'readonly': True},
            {'name': 'notebook',
             'type': 'text',
             'value':  'MyJob1',
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
            {'name': 'run date',
             'type': 'datetime',
             'value': '10/14/2018 18:25:31',
             'readonly': True},
            {'name': 'save',
             'type': 'submit',
             'value': 'Save',
             'url': urljoin(self.config.apiurl, 'notebooks')}
        ])

    def store(self, req, resp):
        name = req.get_param('name')
        nb_name = req.get_param('notebook')
        rp_name = req.get_param('report')
        resp.content_type = 'application/json'
        resp.body = json.dumps([
            {'type': 'h2',
             'value': 'Success!'},
            {'type': 'p',
             'value': 'Successfully configured report {}'.format(name)},
            {'type': 'p',
             'value': 'Notebook: {}'.format(nb_name)},
            {'type': 'p',
             'value': 'Report: {}'.format(rp_name)}])
