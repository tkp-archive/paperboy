from paperboy.config import Report
from paperboy.storage import ReportStorage


class ReportSQLStorage(ReportStorage):
    def form(self):
        return Report(self.config).form()

    def list(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'

    def detail(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'

    def store(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = '{}'
