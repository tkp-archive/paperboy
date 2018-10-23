from .base import BaseResource


class NotebookResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(NotebookResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        self.db.notebooks.list(req, resp, self.session)

    def on_post(self, req, resp):
        self.db.notebooks.store(req, resp, self.session)


class NotebookDetailResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(NotebookDetailResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        self.db.notebooks.detail(req, resp, self.session)
