import json
from .base import BaseResource


class NotebookResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(NotebookResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps(self.db.notebooks.list(req.context['user'], req.params, self.session))

    def on_post(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps(self.db.notebooks.store(req.context['user'], req.params, self.session))


class NotebookDetailResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(NotebookDetailResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps(self.db.notebooks.detail(req.context['user'], req.params, self.session))
