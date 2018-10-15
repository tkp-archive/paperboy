import json
from random import randint
from .base import BaseResource


class JobQuickBrowserResource(BaseResource):
    def __init__(self, db):
        super(JobQuickBrowserResource, self).__init__(db)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({'page': 1,
                                'pages': 15,
                                'count': 10,
                                'total': 150,
                                'jobs': [
                                        {'name': 'TestJob%d' % i,
                                         'meta': {}
                                         } for i in range(10)
                                ]})


class JobResource(BaseResource):
    def __init__(self, db):
        super(JobResource, self).__init__(db)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({'page': 1,
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
                                ]})
