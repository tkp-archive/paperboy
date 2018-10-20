from .base import BaseResource


class JobResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(JobResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        self.db.jobs.list(req, resp)

    def on_post(self, req, resp):
        self.db.jobs.store(req, resp)


class JobDetailResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(JobDetailResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        self.db.jobs.detail(req, resp)
