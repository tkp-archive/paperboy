import falcon
from ..resources import StaticResource, HTMLResource, StatusResource, AutocompleteResource, ConfigResource
from ..resources import NotebookResource, JobResource, ReportResource
from ..resources import NotebookQuickBrowserResource, JobQuickBrowserResource, ReportQuickBrowserResource
from ..middleware import HandleCORS
from ..storage import StorageEngine, StorageError
API = '/api/v1/'


def FalconAPI(config):
    api = falcon.API(middleware=[HandleCORS()] + config.extra_middleware)

    ###########
    # Storage #
    ###########
    db = StorageEngine(config.notebook_storage, config.job_storage, config.report_storage)
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
    status = StatusResource(config, db)
    api.add_route(API + 'status', status)

    # Autocomplete
    autocomplete = AutocompleteResource(config, db)
    api.add_route(API + 'autocomplete', autocomplete)

    # Config
    configresource = ConfigResource(config, db)
    api.add_route(API + 'config', configresource)

    # Notebooks
    notebooks = NotebookResource(config, db)
    api.add_route(API + 'notebooks', notebooks)

    notebooksqb = NotebookQuickBrowserResource(config, db)
    api.add_route(API + 'notebooksqb', notebooksqb)

    # Jobs
    jobs = JobResource(config, db)
    api.add_route(API + 'jobs', jobs)

    jobsqb = JobQuickBrowserResource(config, db)
    api.add_route(API + 'jobsqb', jobsqb)

    # Reports
    reports = ReportResource(config, db)
    api.add_route(API + 'reports', reports)

    reportsqb = ReportQuickBrowserResource(config, db)
    api.add_route(API + 'reportsqb', reportsqb)

    # Extra handlers
    for route, handler in config.extra_handlers:
        api.add_route(route, handler)
    return api
