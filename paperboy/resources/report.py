from .base import BaseResource


class ReportResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(ReportResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        self.db.reports.list(req, resp, self.session)

    def on_post(self, req, resp):
        self.db.reports.store(req, resp, self.session)


class ReportDetailResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(ReportDetailResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        self.db.reports.detail(req, resp, self.session)
