import json
from .base import BaseResource


class StatusResource(BaseResource):
    def __init__(self, db):
        super(StatusResource, self).__init__(db)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({'notebooks': {
                                    'total': 25,
                                    'production': 15,
                                    'research': 3,
                                    'mine': 7},
                                'jobs': {
                                    'total': 150,
                                    'done': 25,
                                    'running': 10,
                                    'queue': 60,
                                    'disabled': 55},
                                'reports': {
                                    'total': 3250,
                                    'published': 2074,
                                    'unpublished': 276,
                                    'public': 2755,
                                    'private': 495}
                                })
