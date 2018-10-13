import json
from .base import BaseResource


class NotebookResource(BaseResource):
    def __init__(self, db):
        super(NotebookResource, self).__init__(db)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({'page': 0,
                                'count': 10,
                                'total': 25,
                                'notebooks': [
                                        {'name': 'TestNB%d' % i,
                                         'meta': {}
                                         } for i in range(10)
                                ]})

    def on_post(self, req, resp):
        resp.content_type = 'application/json'
