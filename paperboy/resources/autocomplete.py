import json
from .base import BaseResource


class AutocompleteResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(AutocompleteResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        partial = req.params.get('partial', None)
        type = req.params.get('type', None)

        if type is None:
            resp.body = json.dumps(self.db.notebooks.search(10, name=partial, session=self.session) +
                                   self.db.jobs.search(10, name=partial, session=self.session) +
                                   self.db.reports.search(10, name=partial, session=self.session))

        elif type == 'notebooks':
            resp.body = json.dumps(self.db.notebooks.search(10, name=partial, session=self.session))
        elif type == 'jobs':
            resp.body = json.dumps(self.db.jobs.search(10, name=partial, session=self.session))
        elif type == 'reports':
            resp.body = json.dumps(self.db.reports.search(10, name=partial, session=self.session))
        else:
            resp.body = 'No results for type {}'.format(type)
