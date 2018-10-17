import falcon
from six.moves.urllib_parse import urljoin
from ..resources import StaticResource, HTMLResource, StatusResource, AutocompleteResource, ConfigResource
from ..resources import NotebookResource, JobResource, ReportResource
from ..resources import NotebookQuickBrowserResource, JobQuickBrowserResource, ReportQuickBrowserResource
from ..middleware import CORSMiddleware, MultipartMiddleware, JSONMiddleware, AuthMiddleware, auth_backend
from ..storage import StorageEngine, StorageError


def FalconAPI(config):
    api = falcon.API(middleware=[CORSMiddleware(allow_all_origins=True).middleware,
                                 MultipartMiddleware(),
                                 # JSONMiddleware(),
                                 # AuthMiddleware(auth_backend
                                 ] +
                     config.extra_middleware)

    ###########
    # Storage #
    ###########
    db = StorageEngine(config.notebook_storage(config), config.job_storage(config), config.report_storage(config))
    api.add_error_handler(StorageError, StorageError.handle)

    ####################
    # Static resources #
    ####################
    html = HTMLResource(config)
    static = StaticResource(config)
    api.add_route('/', html)
    api.add_route('/index.html', html)
    api.add_sink(static.on_get, prefix='/static')

    ##########
    # Routes #
    ##########
    # Status
    status = StatusResource(config, db)
    api.add_route(config.apiurl + 'status', status)

    # Autocomplete
    autocomplete = AutocompleteResource(config, db)
    api.add_route(urljoin(config.apiurl, 'autocomplete'), autocomplete)

    # Config
    configresource = ConfigResource(config, db)
    api.add_route(urljoin(config.apiurl, 'config'), configresource)

    # Notebooks
    notebooks = NotebookResource(config, db)
    api.add_route(urljoin(config.apiurl, 'notebooks'), notebooks)

    notebooksqb = NotebookQuickBrowserResource(config, db)
    api.add_route(urljoin(config.apiurl, 'notebooksqb'), notebooksqb)

    # Jobs
    jobs = JobResource(config, db)
    api.add_route(urljoin(config.apiurl, 'jobs'), jobs)

    jobsqb = JobQuickBrowserResource(config, db)
    api.add_route(urljoin(config.apiurl, 'jobsqb'), jobsqb)

    # Reports
    reports = ReportResource(config, db)
    api.add_route(urljoin(config.apiurl, 'reports'), reports)

    reportsqb = ReportQuickBrowserResource(config, db)
    api.add_route(urljoin(config.apiurl, 'reportsqb'), reportsqb)

    # Extra handlers
    for route, handler in config.extra_handlers:
        api.add_route(route, handler)
    return api
