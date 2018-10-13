import json
from .base import BaseResource


class StatusResource(BaseResource):
    def __init__(self, db):
        super(StatusResource, self).__init__(db)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({'notebooks': 25, 'jobs': 150, 'reports': 3520})
