import json
from .base import BaseResource


class NotebookResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(NotebookResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps(self.db.notebooks.list())

    def on_post(self, req, resp):
        self.db.notebooks.store(req, resp)


class NotebookDetailResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(NotebookDetailResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        json.dumps(self.db.notebooks.detail(req, resp))
