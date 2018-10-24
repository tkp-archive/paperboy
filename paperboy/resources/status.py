import json
from .base import BaseResource


class StatusResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(StatusResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        type = req.params.get('type', '')
        if type == 'notebooks':
            resp.body = json.dumps(self.db.notebooks.status(self.session))
        elif type == 'jobs':
            resp.body = json.dumps(self.db.jobs.status(self.session))
        elif type == 'reports':
            resp.body = json.dumps(self.db.reports.status(self.session))
        else:
            ret = {}
            ret['notebooks'] = self.db.notebooks.status(self.session)
            ret['jobs'] = self.db.jobs.status(self.session)
            ret['reports'] = self.db.reports.status(self.session)
            resp.body = json.dumps(ret)
