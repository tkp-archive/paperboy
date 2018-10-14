import json
from .base import BaseResource


class AutocompleteResource(BaseResource):
    def __init__(self, db):
        super(AutocompleteResource, self).__init__(db)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps([{'key': 'TestKey{}'.format(i),
                                 'name': 'TestName{}'.format(i)}
                                for i in range(10)
                                ])

    def on_post(self, req, resp):
        resp.content_type = 'application/json'
