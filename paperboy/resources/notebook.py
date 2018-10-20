from .base import BaseResource


class NotebookResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(NotebookResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        self.db.notebooks.list(req, resp)

    def on_post(self, req, resp):
        self.db.notebooks.store(req, resp)


class NotebookDetailResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(NotebookDetailResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        self.db.notebooks.detail(req, resp)
