import falcon
from six.moves.urllib_parse import urljoin
from ..resources import StaticResource, HTMLResource, LoginResource, LogoutResource, StatusResource, AutocompleteResource, ConfigResource
from ..resources import NotebookResource, JobResource, ReportResource
from ..resources import NotebookDetailResource, JobDetailResource, ReportDetailResource
from ..storage import StorageEngine, StorageError


def FalconAPI(config):
    api = falcon.API(middleware=[config.auth_required_mw(config, when_fails=config._login_redirect),
                                 config.load_user_mw(config)] +
                     config.essential_middleware +
                     config.extra_middleware)

    def from_base(url):
        return urljoin(config.baseurl, url)

    def from_api(url):
        return urljoin(config.apiurl, url)

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
    api.add_route(from_base(''), html)
    api.add_route(from_base('index.html'), html)
    api.add_sink(static.on_get, prefix=from_base('static'))

    ##################
    # Auth Resources #
    ##################
    login = LoginResource(config)
    api.add_route(from_base(config.loginurl), login)
    logout = LogoutResource(config)
    api.add_route(from_base(config.logouturl), logout)

    ##########
    # Routes #
    ##########
    kwargs = {'config': config,
              'db': db,
              'scheduler': scheduler}

    # Status
    status = StatusResource(**kwargs)
    api.add_route(from_api('status'), status)

    # Autocomplete
    autocomplete = AutocompleteResource(**kwargs)
    api.add_route(from_api('autocomplete'), autocomplete)

    # Config
    configresource = ConfigResource(**kwargs)
    api.add_route(from_api('config'), configresource)

    # Notebooks
    notebooks = NotebookResource(**kwargs)
    api.add_route(from_api('notebooks'), notebooks)

    notebooksdetail = NotebookDetailResource(**kwargs)
    api.add_route(from_api('notebooks/details'), notebooksdetail)

    # Jobs
    jobs = JobResource(**kwargs)
    api.add_route(from_api('jobs'), jobs)

    jobdetail = JobDetailResource(**kwargs)
    api.add_route(from_api('jobs/details'), jobdetail)

    # Reports
    reports = ReportResource(**kwargs)
    api.add_route(from_api('reports'), reports)

    reportdetail = ReportDetailResource(**kwargs)
    api.add_route(from_api('reports/details'), reportdetail)

    # Extra handlers
    for route, handler in config.extra_handlers:
        api.add_route(route, handler(**kwargs))
    return api
