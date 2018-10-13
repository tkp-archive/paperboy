import json
from .base import BaseResource


class ReportResource(BaseResource):
    def __init__(self, db):
        super(ReportResource, self).__init__(db)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({'page': 0,
                                'count': 10,
                                'total': 3520,
                                'reports': [
                                        {'name': 'TestReport%d' % i,
                                         'meta': {}
                                         } for i in range(10)
                                ]})

    def on_post(self, req, resp):
        resp.content_type = 'application/json'
