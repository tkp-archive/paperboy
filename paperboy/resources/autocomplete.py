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
            resp.body = json.dumps([{'id': 'Notebook-{}'.format(i),
                                     'name': 'MyNotebook{}'.format(i)}
                                    for i in range(20)
                                    ] +
                                   [{'id': 'Job-{}'.format(i),
                                     'name': 'MyJob{}'.format(i)}
                                    for i in range(20)
                                    ] +
                                   [{'id': 'Report-{}'.format(i),
                                     'name': 'MyReport{}'.format(i)}
                                    for i in range(20)
                                    ])

        elif type == 'notebooks':
            resp.body = json.dumps([{'id': i, 'name': 'TestNB{}'.format(i)} for i in range(20)])
        elif type == 'jobs':
            resp.body = json.dumps([{'id': i, 'name': 'TestJob{}'.format(i)} for i in range(20)])
        elif type == 'reports':
            resp.body = json.dumps([{'id': i, 'name': 'TestReport{}'.format(i)} for i in range(20)])
        else:
            resp.body = 'No results for type {}'.format(type)
