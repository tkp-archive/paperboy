import json
from .base import BaseResource


class AutocompleteResource(BaseResource):
    def __init__(self, *args):
        super(AutocompleteResource, self).__init__(*args)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        partial = req.params.get('partial', None)
        type = req.params.get('type', None)
        if type is None:
            resp.body = json.dumps([{'key': 'TestKey{}'.format(i),
                                     'name': 'TestName{}'.format(i)}
                                    for i in range(10)
                                    ])
        elif type == 'notebooks':
            resp.body = json.dumps([{'key': i, 'name': 'TestNB{}'.format(i)} for i in range(20)])
        elif type == 'jobs':
            resp.body = json.dumps([{'key': i, 'name': 'TestJob{}'.format(i)} for i in range(20)])
        elif type == 'reports':
            resp.body = json.dumps([{'key': i, 'name': 'TestReport{}'.format(i)} for i in range(20)])
        else:
            resp.body = 'No results for type {}'.format(type)

    def on_post(self, req, resp):
        resp.content_type = 'application/json'
