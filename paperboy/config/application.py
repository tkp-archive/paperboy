import falcon
import logging
import os

from ..storage import NotebookStorage, JobStorage, ReportStorage
from ..storage.dummy import NotebookDummyStorage, JobDummyStorage, ReportDummyStorage
from ..scheduler import DummyScheduler
from ..server.api import FalconAPI
from ..server.deploy import FalconGunicorn

from traitlets.config.application import Application
from traitlets import Int, Instance, List, Tuple, Type, Unicode


class Paperboy(Application):
    """Base class for paperboy applications"""
    name = 'paperboy'
    description = "paperboy"

    workers = Int(default_value=2)
    port = Unicode(default_value='8080')

    api = Instance(falcon.API)

    baseurl = Unicode(default_value='/')
    apiurl = Unicode(default_value='/api/v1/')

    ################################################
    # FIXME doesnt allow default_value yet         #
    # notebook_storage = Type(NotebookStorage, default_value=NotebookDummyStorage)
    # job_storage = Type(JobStorage, default_value=JobDummyStorage)
    # report_storage = Type(ReportStorage, default_value=ReportDummyStorage)
    notebook_storage = NotebookDummyStorage
    job_storage = JobDummyStorage
    report_storage = ReportDummyStorage
    #                                              #
    scheduler = DummyScheduler
    # END                                          #
    ################################################

    extra_middleware = List(default_value=[])  # List of extra middlewares to install
    extra_handlers = List(trait=Tuple(), default_value=[])  # List of tuples (route, handler) of handlers to install

    def _log_level_default(self):
        return logging.INFO

    def start(self):
        """Start the whole thing"""
        self.port = os.environ.get('PORT', self.port)
        options = {
            'bind': '0.0.0.0:{}'.format(self.port),
            'workers': self.workers
        }
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
