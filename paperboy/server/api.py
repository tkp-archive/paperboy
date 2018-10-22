import falcon
from six.moves.urllib_parse import urljoin
from ..resources import StaticResource, HTMLResource, LoginResource, StatusResource, AutocompleteResource, ConfigResource
from ..resources import NotebookResource, JobResource, ReportResource
from ..resources import NotebookDetailResource, JobDetailResource, ReportDetailResource
from ..storage import StorageEngine, StorageError


def FalconAPI(config):
    api = falcon.API(middleware=[config.authrequired(when_fails=config._login_redirect),
                                 config.loaduser()] +
                     config.essential_middleware +
                     config.extra_middleware)

    ###########
    # Storage #
    ###########
    db = StorageEngine(config.notebook_storage(config), config.job_storage(config), config.report_storage(config))
    api.add_error_handler(StorageError, StorageError.handle)

    #############
    # Scheduler #
    #############
    scheduler = config.scheduler(config)

    ####################
    # Static resources #
    ####################
    html = HTMLResource(config)
    static = StaticResource(config)
    api.add_route('/', html)
    api.add_route('/index.html', html)
    api.add_sink(static.on_get, prefix='/static')

    ##################
    # Auth Resources #
    ##################
    login = LoginResource(config)
    api.add_route('/login', login)

    ##########
    # Routes #
    ##########
    kwargs = {'config': config,
              'db': db,
              'scheduler': scheduler}

    # Status
    status = StatusResource(**kwargs)
    api.add_route(config.apiurl + 'status', status)

    # Autocomplete
    autocomplete = AutocompleteResource(**kwargs)
    api.add_route(urljoin(config.apiurl, 'autocomplete'), autocomplete)

    # Config
    configresource = ConfigResource(**kwargs)
    api.add_route(urljoin(config.apiurl, 'config'), configresource)

    # Notebooks
    notebooks = NotebookResource(**kwargs)
    api.add_route(urljoin(config.apiurl, 'notebooks'), notebooks)

    notebooksdetail = NotebookDetailResource(**kwargs)
    api.add_route(urljoin(config.apiurl, 'notebooks/details'), notebooksdetail)

    # Jobs
    jobs = JobResource(**kwargs)
    api.add_route(urljoin(config.apiurl, 'jobs'), jobs)

    jobdetail = JobDetailResource(**kwargs)
    api.add_route(urljoin(config.apiurl, 'jobs/details'), jobdetail)

    # Reports
    reports = ReportResource(**kwargs)
    api.add_route(urljoin(config.apiurl, 'reports'), reports)

    reportdetail = ReportDetailResource(**kwargs)
    api.add_route(urljoin(config.apiurl, 'reports/details'), reportdetail)

    # Extra handlers
    for route, handler in config.extra_handlers:
        api.add_route(route, handler(**kwargs))
    return api
