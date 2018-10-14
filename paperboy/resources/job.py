import json
from .base import BaseResource


class JobResource(BaseResource):
    def __init__(self, db):
        super(JobResource, self).__init__(db)

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

    def on_post(self, req, resp):
        resp.content_type = 'application/json'
