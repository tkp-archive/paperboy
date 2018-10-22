import falcon
import logging
import os
from six.moves.urllib_parse import urljoin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from traitlets.config.application import Application
from traitlets import Int, Instance, List, Tuple, Unicode, Bool, validate, TraitError

# falcon api
from ..server.api import FalconAPI

# gunicorn deployer
from ..server.deploy import FalconGunicorn

# base classes
from ..storage import UserStorage, NotebookStorage, JobStorage, ReportStorage

# dummy
from ..storage.dummy import UserDummyStorage, NotebookDummyStorage, JobDummyStorage, ReportDummyStorage
from ..scheduler import DummyScheduler
from ..middleware import DummyUserMiddleware, DummyAuthRequiredMiddleware

# no auth
from ..middleware import NoUserMiddleware, NoAuthRequiredMiddleware

# essential middleware
from ..middleware import CORSMiddleware, MultipartMiddleware

# sql
from ..storage.sqla import UserSQLStorage, NotebookSQLStorage, JobSQLStorage, ReportSQLStorage
from ..middleware import SQLAlchemySessionMiddleware


class Paperboy(Application):
    """Base class for paperboy applications"""
    name = 'paperboy'
    description = 'paperboy'

    ############
    # Gunicorn #
    ############
    workers = Int(default_value=2)
    port = Unicode(default_value='8080')
    ############

    ##########
    # Falcon #
    ##########
    api = Instance(falcon.API)
    ##########

    ########
    # URLs #
    ########
    baseurl = Unicode(default_value='/')
    apiurl = Unicode(default_value='/api/v1/')
    loginurl = Unicode(default_value='login')
    logouturl = Unicode(default_value='logout')
    registerurl = Unicode(default_value='register')
    ########

    #############
    # Misc Auth #
    #############
    http = Bool(default_value=True)
    include_password = Bool(default_value=False)
    include_register = Bool(default_value=True)
    token_timeout = Int(default_value=600)
    #############

    def _login_redirect(config, *args, **kwargs):
        raise falcon.HTTPFound(urljoin(config.baseurl, config.loginurl))

    ################################################
    # FIXME doesnt allow default_value yet         #
    user_storage = UserDummyStorage
    notebook_storage = NotebookDummyStorage
    job_storage = JobDummyStorage
    report_storage = ReportDummyStorage
    #                                              #
    scheduler = DummyScheduler
    #                                              #
    auth_required_mw = Instance(object)
    load_user_mw = Instance(object)
    # END                                          #
    ################################################

    ##############
    # Middleware #
    ##############
    essential_middleware = [CORSMiddleware(allow_all_origins=True).middleware,
                            MultipartMiddleware()]
    extra_middleware = List(default_value=[])  # List of extra middlewares to install
    ##############

    ##################
    # Custom handler #
    ##################
    extra_handlers = List(trait=Tuple(), default_value=[])  # List of tuples (route, handler) of handlers to install
    ##################

    ##########################################
    #        Predefined Configurations       #
    #
    ##########################################
    backend = Unicode(default_value='dummy')
    auth = Unicode(default_value='dummy')

    @validate('backend')
    def _validate_backend(self, proposed):
        if proposed['value'] not in ('custom', 'dummy', 'git', 'sqla',):
            raise TraitError('backend not recognized: %s'.format(proposed['value']))
        return proposed['value']

    @validate('auth')
    def _validate_auth(self, proposed):
        if proposed['value'] not in ('custom', 'dummy', 'none', 'sqla',):
            raise TraitError('backend not recognized: %s'.format(proposed['value']))
        return proposed['value']
    ##########################################

    ##############
    # SQL extras #
    ##############
    sql_url = 'sqlite:///:memory:'
    engine = None
    sessionmaker = None
    sql_user = Bool(default_value=True)
    ##############

    def start(self):
        """Start the whole thing"""
        self.port = os.environ.get('PORT', self.port)
        options = {
            'bind': '0.0.0.0:{}'.format(self.port),
            'workers': self.workers
        }

        # Preconfigured storage backends
        if self.backend == 'git':
            logging.critical('Using Git backend')
            raise NotImplemented

        elif self.backend == 'sqla':
            logging.critical('Using SQL backend')
            self.engine = create_engine(self.sql_url, echo=True)
            self.sessionmaker = sessionmaker(bind=self.engine)
            self.extra_middleware = self.extra_middleware + [SQLAlchemySessionMiddleware(self.sessionmaker())]
            self.user_storage = UserSQLStorage
            self.sql_user = True
            self.notebook_storage = NotebookSQLStorage
            self.job_storage = JobSQLStorage
            self.report_storage = ReportSQLStorage

        elif self.backend == 'dummy':
            logging.critical('Using Dummy backend')
            self.user_storage = UserDummyStorage
            self.notebook_storage = NotebookDummyStorage
            self.job_storage = JobDummyStorage
            self.report_storage = ReportDummyStorage
            self.sql_user = False

        # Preconfigured auth backends
        if self.auth == 'none':
            logging.critical('Using No auth')
            self.auth_required_mw = NoAuthRequiredMiddleware
            self.load_user_mw = NoUserMiddleware

        elif self.auth == 'sqla':
            logging.critical('Using SQL auth')
            raise NotImplemented

        elif self.auth == 'dummy':
            logging.critical('Using Dummy auth')
            self.auth_required_mw = DummyAuthRequiredMiddleware
            self.load_user_mw = DummyUserMiddleware

        FalconGunicorn(FalconAPI(self), options).run()

    @classmethod
    def launch_instance(cls, argv=None, **kwargs):
        """Launch an instance of a Paperboy Application"""
        return super(Paperboy, cls).launch_instance(argv=argv, **kwargs)

    def to_dict(self):
        return {'name': self.name,
                'description': self.description,
                'workers': self.workers,
                'port': self.port}
