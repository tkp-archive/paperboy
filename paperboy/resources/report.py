import json
from .base import BaseResource


class ReportQuickBrowserResource(BaseResource):
    def __init__(self, *args):
        super(ReportQuickBrowserResource, self).__init__(*args)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps(self.db.reports.status())


class ReportResource(BaseResource):
    def __init__(self, *args):
        super(ReportResource, self).__init__(*args)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps(self.db.reports.list())

    def on_post(self, req, resp):
        self.db.reports.store(req, resp)
