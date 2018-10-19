import json
import nbformat
from random import randint, choice
from six.moves.urllib_parse import urljoin
from paperboy.config import Notebook
from ..base import NotebookStorage


class NotebookDummyStorage(NotebookStorage):
    def object(self):
        return Notebook

    def form(self):
        return [
            {'name': 'file',
             'type': 'file',
             'label': 'File',
             'required': True},
            {'name': 'name',
             'type': 'text',
             'label': 'Name',
             'placeholder': 'Name for Notebook...',
             'required': True},
            {'name': 'privacy',
             'type': 'select',
             'label': 'Visibility',
             'options': ['Private', 'Public'],
             'required': True},
            {'name': 'sla',
             'type': 'select',
             'label': 'SLA',
             'options': ['Production', 'Research', 'Development', 'Personal'],
             'required': True},
            {'name': 'build',
             'type': 'label',
             'label': 'Build options'},
            {'name': 'requirements',
             'type': 'file',
             'label': 'requirements.txt',
             'required': False},
            {'name': 'dockerfile',
             'type': 'file',
             'label': 'Dockerfile',
             'required': False},
            {'name': 'submit',
             'type': 'submit',
             'value': 'Create',
             'url': urljoin(self.config.apiurl, 'notebooks')}
        ]

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
        resp.body = json.dumps([
            {'name': 'name',
             'type': 'text',
             'value': 'MyNotebook',
             'required': True},
            {'name': 'id',
             'type': 'text',
             'value': 'Notebook-1',
             'required': True,
             'readonly': True},
            {'name': 'author',
             'type': 'text',
             'value':  'Joe Python',
             'required': True,
             'readonly': True},
            {'name': 'jobs',
             'type': 'text',
             'value':  '25',
             'readonly': True},
            {'name': 'reports',
             'type': 'text',
             'value':  '353',
             'readonly': True},
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
        name = req.get_param('name')
        nb = nbformat.reads(req.get_param('file').file.read(), 4)
        resp.content_type = 'application/json'
        resp.body = json.dumps([
            {'type': 'h2',
             'value': 'Success!'},
            {'type': 'p',
             'value': 'Successfully stored notebook {}'.format(name)}
        ])
