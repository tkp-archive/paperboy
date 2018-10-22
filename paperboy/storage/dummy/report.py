import json
import logging
from paperboy.config import Report
from paperboy.config.storage import ReportListResult
from paperboy.storage import ReportStorage


class ReportDummyStorage(ReportStorage):
    def form(self):
        return Report(self.config).form()

    def list(self, req, resp):
        resp.content_type = 'application/json'
        result = ReportListResult()
        result.page = 1
        result.pages = 141
        result.count = 25
        result.total = 3520
        result.reports = [
                    Report.from_json(
                        {'name': 'TestReport%d' % i,
                         'id': 'Report-%d' % i,
                         'meta': {
                            # 'notebook': 'TestNotebook',
                            # 'notebookid': 'Notebook-%d' % i,
                            # 'job': 'TestJob',
                            # 'jobid': 'Job-%d' % i,
                            'created': '10/14/2018 04:50:33',
                            'run': '10/14/2018 18:25:31'}},
                        self.config) for i in range(25)
                ]
        resp.body = result.to_json(True)

    def detail(self, req, resp):
        resp.content_type = 'application/json'
        details = Report.from_json(
            {'name': 'TestReport1',
             'id': 'Report-1',
             'meta': {
                # 'notebook': 'TestNotebook',
                # 'notebookid': 'Notebook-%d' % i,
                # 'job': 'TestJob',
                # 'jobid': 'Job-%d' % i,
                'created': '10/14/2018 04:50:33',
                'run': '10/14/2018 18:25:31',
                 }},
            self.config).edit()
        resp.body = json.dumps(details)

    def store(self, req, resp):
        name = req.get_param('name')
        nb_name = req.get_param('notebook')
        rp_name = req.get_param('report')
        resp.content_type = 'application/json'

        store = Report.from_json(
            {'name': 'TestReport1',
             'id': 'Report-1',
             'meta': {
                # 'notebook': 'TestNotebook',
                # 'notebookid': 'Notebook-%d' % i,
                # 'job': 'TestJob',
                # 'jobid': 'Job-%d' % i,
                'created': '10/14/2018 04:50:33',
                'run': '10/14/2018 18:25:31',
                 }},
            self.config).store()
        logging.critical("Storing job {}".format(name))
        resp.body = json.dumps(store)
