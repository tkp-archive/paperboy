import json
from .base import BaseResource


class JobQuickBrowserResource(BaseResource):
    def __init__(self, *args):
        super(JobQuickBrowserResource, self).__init__(*args)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps(self.db.jobs.status())


class JobResource(BaseResource):
    def __init__(self, *args):
        super(JobResource, self).__init__(*args)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps(self.db.jobs.detail())
