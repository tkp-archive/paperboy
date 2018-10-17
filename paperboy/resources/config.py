import falcon
import json
from .base import BaseResource


class ConfigResource(BaseResource):
    def __init__(self, *args):
        super(ConfigResource, self).__init__(*args)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        type = req.params.get('type', None)
        if type is None:
            resp.body = json.dumps(self.config.to_dict())
        elif type == 'notebooks':
            resp.body = json.dumps(self.db.notebooks.form())
        elif type == 'jobs':
            resp.body = json.dumps(self.db.jobs.form())
        elif type == 'reports':
            resp.body = json.dumps(self.db.reports.form())
        else:
            resp.status = falcon.HTTP_404
