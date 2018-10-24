from .base import BaseResource


class SchedulerResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(SchedulerResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        self.scheduler.status(req, resp, self.session)
