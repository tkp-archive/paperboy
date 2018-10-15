import falcon
from ..resources import StaticResource, HTMLResource, StatusResource, AutocompleteResource
from ..resources import NotebookResource, JobResource, ReportResource
from ..resources import NotebookQuickBrowserResource, JobQuickBrowserResource, ReportQuickBrowserResource
from ..middleware import HandleCORS
from ..storage import StorageEngine, StorageError
API = '/api/v1/'


def FalconAPI():
    api = falcon.API(middleware=[HandleCORS()])

    ###########
    # Storage #
    ###########
    db = StorageEngine()
    api.add_error_handler(StorageError, StorageError.handle)

    ####################
    # Static resources #
    ####################
    html = HTMLResource()
    static = StaticResource()
    api.add_route('/', html)
    api.add_route('/index.html', html)
    api.add_sink(static.on_get, prefix='/static')

    ##########
    # Routes #
    ##########
    # Status
    status = StatusResource(db)
    api.add_route(API + 'status', status)

    # Autocomplete
    autocomplete = AutocompleteResource(db)
    api.add_route(API + 'autocomplete', autocomplete)

    # Notebooks
    notebooks = NotebookResource(db)
    api.add_route(API + 'notebooks', notebooks)

    notebooksqb = NotebookQuickBrowserResource(db)
    api.add_route(API + 'notebooksqb', notebooksqb)

    # Jobs
    jobs = JobResource(db)
    api.add_route(API + 'jobs', jobs)

    jobsqb = JobQuickBrowserResource(db)
    api.add_route(API + 'jobsqb', jobsqb)

    # Reports
    reports = ReportResource(db)
    api.add_route(API + 'reports', reports)

    reportsqb = ReportQuickBrowserResource(db)
    api.add_route(API + 'reportsqb', reportsqb)
    return api
