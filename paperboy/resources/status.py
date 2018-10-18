from .base import BaseResource


class StatusResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(StatusResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        self.scheduler.status(req, resp)
