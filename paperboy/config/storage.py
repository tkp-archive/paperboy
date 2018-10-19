import json
from .base import Notebook, Job, Report
from .forms import Form, Response
from traitlets import List, Int, TraitType


class ListResult(TraitType):
    page = Int(default_value=1)
    pages = Int(default_value=1)
    count = Int(default_value=1)
    total = Int(default_value=1)

    def to_json(self, string=False):
        ret = {}
        ret['page'] = self.page
        ret['pages'] = self.pages
        ret['count'] = self.count
        ret['total'] = self.total
        if string:
            return json.dumps(ret)
        return ret


class NotebookListResult(ListResult):
    notebooks = List(trait=Notebook)

    def to_json(self, string=False):
        ret = super(NotebookListResult, self).to_json()
        ret['notebooks'] = [nb.to_json() for nb in self.notebooks]
        if string:
            return json.dumps(ret)
        return ret


class JobListResult(ListResult):
    jobs = List(trait=Job)

    def to_json(self, string=False):
        ret = super(JobListResult, self).to_json()
        ret['jobs'] = [jb.to_json() for jb in self.jobs]
        if string:
            return json.dumps(ret)
        return ret


class ReportListResult(ListResult):
    reports = List(trait=Report)

    def to_json(self, string=False):
        ret = super(ReportListResult, self).to_json()
        ret['reports'] = [rp.to_json() for rp in self.reports]
        if string:
            return json.dumps(ret)
        return ret


class DetailResult(Form):
    pass


class StoreResult(Response):
    pass
