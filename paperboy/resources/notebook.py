import json
from .base import BaseResource


class NotebookQuickBrowserResource(BaseResource):
    def __init__(self, *args):
        super(NotebookQuickBrowserResource, self).__init__(*args)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps(self.db.notebooks.status())


class NotebookResource(BaseResource):
    def __init__(self, *args):
        super(NotebookResource, self).__init__(*args)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps(self.db.notebooks.list())

    def on_post(self, req, resp):
        self.db.notebooks.store(req, resp)
