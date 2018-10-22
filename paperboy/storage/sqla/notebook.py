from paperboy.config import Notebook
from paperboy.storage import NotebookStorage


class NotebookSQLStorage(NotebookStorage):
    def form(self):
        return Notebook(self.config).form()

    def list(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'

    def detail(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'

    def store(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'
