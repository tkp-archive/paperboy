import falcon
from ..resources import StaticResource, HTMLResource, StatusResource, NotebookResource, JobResource, ReportResource, AutocompleteResource
from ..middleware import HandleCORS
from ..storage import StorageEngine, StorageError
API = '/api/v1/'


def FalconAPI():
    api = falcon.API(middleware=[HandleCORS()])

    # database
    db = StorageEngine()
    api.add_error_handler(StorageError, StorageError.handle)

    # Static resources
    html = HTMLResource()
    static = StaticResource()
    api.add_route('/', html)
    api.add_route('/index.html', html)
    api.add_sink(static.on_get, prefix='/static')

    # Routes
    status = StatusResource(db)
    api.add_route(API + 'status', status)

    notebooks = NotebookResource(db)
    api.add_route(API + 'notebooks', notebooks)

    jobs = JobResource(db)
    api.add_route(API + 'jobs', jobs)

    reports = ReportResource(db)
    api.add_route(API + 'reports', reports)

    autocomplete = AutocompleteResource(db)
    api.add_route(API + 'autocomplete', autocomplete)
    return api
