import json


class StatusResource(object):
    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({'notebooks': 25, 'jobs': 150, 'reports': 3520})
