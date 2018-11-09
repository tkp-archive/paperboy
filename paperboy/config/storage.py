import json
from traitlets import List, Int, HasTraits, Instance
from .base import Base


class ListResult(HasTraits):
    page = Int(default_value=1)
    pages = Int(default_value=1)
    count = Int(default_value=1)
    total = Int(default_value=1)
    results = List(trait=Instance(Base))

    def to_json(self):
        ret = {}
        ret['page'] = self.page
        ret['pages'] = self.pages
        ret['count'] = self.count
        ret['total'] = self.total
        ret['results'] = [r.to_json() for r in self.results]
        return ret
