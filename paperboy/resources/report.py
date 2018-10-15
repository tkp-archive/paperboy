import json
from random import randint, choice
from .base import BaseResource


class ReportQuickBrowserResource(BaseResource):
    def __init__(self, db):
        super(ReportQuickBrowserResource, self).__init__(db)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({'page': 1,
                                'pages': 352,
                                'count': 10,
                                'total': 3520,
                                'reports': [
                                        {'name': 'TestReport%d' % i,
                                         'meta': {}
                                         } for i in range(10)
                                ]})


class ReportResource(BaseResource):
    def __init__(self, db):
        super(ReportResource, self).__init__(db)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({'page': 1,
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
                                ]})
