import falcon
import json
import nbformat
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
        resp.body = json.dumps(self.db.notebooks.detail())

    def on_post(self, req, resp):
        name = req.get_param('name')
        nb = nbformat.reads(req.get_param('file').file.read(), 4)
        print(nb)
        # raise falcon.HTTPSeeOther('/')
        resp.content_type = 'application/json'
        resp.body = nbformat.writes(nb)
