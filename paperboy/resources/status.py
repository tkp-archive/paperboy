import json
from .base import BaseResource


class StatusResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(StatusResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        type = req.params.get('type', '')
        if type == 'notebooks':
            resp.body = json.dumps(self.db.notebooks.status())
        elif type == 'jobs':
            resp.body = json.dumps(self.db.jobs.status())
        elif type == 'reports':
            resp.body = json.dumps(self.db.reports.status())
        else:
            ret = {}
            ret['notebooks'] = self.db.notebooks.status()
            ret['jobs'] = self.db.jobs.status()
            ret['reports'] = self.db.reports.status()
            resp.body = json.dumps(ret)
