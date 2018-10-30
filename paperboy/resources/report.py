import json
from .base import BaseResource


class ReportResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(ReportResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        req.context['params'] = req.params
        resp.body = json.dumps(self.db.reports.list(req.context, self.session))

    def on_post(self, req, resp):
        resp.content_type = 'application/json'
        req.context['params'] = req.params
        resp.body = json.dumps(self.db.reports.store(req.context, self.session))


class ReportDetailResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(ReportDetailResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        req.context['params'] = req.params
        resp.body = json.dumps(self.db.reports.detail(req.context, self.session))
