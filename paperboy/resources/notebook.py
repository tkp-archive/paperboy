import json
from random import randint, choice
from .base import BaseResource


class NotebookQuickBrowserResource(BaseResource):
    def __init__(self, db):
        super(NotebookQuickBrowserResource, self).__init__(db)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({'page': 1,
                                'pages': 3,
                                'count': 10,
                                'total': 25,
                                'notebooks': [
                                        {'name': 'TestNB%d' % i,
                                         'meta': {}
                                         } for i in range(10)
                                ]})


class NotebookResource(BaseResource):
    def __init__(self, db):
        super(NotebookResource, self).__init__(db)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({'page': 1,
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
                                            'last modified': '10/14/2018 18:25:31',
                                         }
                                         } for i in range(25)
                                ]})
