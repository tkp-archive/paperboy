from .job import Job
from .notebook import Notebook
from .report import Report
from traitlets import List, Int, HasTraits, Instance


class ListResult(HasTraits):
    page = Int(default_value=1)
    pages = Int(default_value=1)
    count = Int(default_value=1)
    total = Int(default_value=1)

    def to_json(self):
        ret = {}
        ret['page'] = self.page
        ret['pages'] = self.pages
        ret['count'] = self.count
        ret['total'] = self.total
        return ret


class NotebookListResult(ListResult):
    notebooks = List(trait=Instance(Notebook))

    def to_json(self):
        ret = super(NotebookListResult, self).to_json()
        ret['notebooks'] = [nb.to_json() for nb in self.notebooks]
        return ret


class JobListResult(ListResult):
    jobs = List(trait=Instance(Job))

    def to_json(self):
        ret = super(JobListResult, self).to_json()
        ret['jobs'] = [jb.to_json() for jb in self.jobs]
        return ret


class ReportListResult(ListResult):
    reports = List(trait=Instance(Report))

    def to_json(self):
        ret = super(ReportListResult, self).to_json()
        ret['reports'] = [rp.to_json() for rp in self.reports]
        return ret
