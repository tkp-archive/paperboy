import sys
from mock import patch, MagicMock


class TestConfig:
    def test_import1(self):
        from paperboy import __version__

    def test_import2(self):
        from paperboy.config import User, Notebook, Job, Report

    # def test_import3(self):
    #     from paperboy.client import

    def test_import4(self):
        from paperboy.middleware import CORSMiddleware, AuthRequiredMiddleware, LoadUserMiddleware, MultipartMiddleware, DummyUserMiddleware, DummyAuthRequiredMiddleware, NoUserMiddleware, NoAuthRequiredMiddleware, SQLUserMiddleware, SQLAuthRequiredMiddleware, SQLAlchemySessionMiddleware

    def test_import5(self):
        from paperboy.resources import AutocompleteResource, ConfigResource, HTMLResource, JobResource, JobDetailResource, LoginResource, LogoutResource, NotebookResource, NotebookDetailResource, RegisterResource, ReportResource, ReportDetailResource, StaticResource, StatusResource

    def test_import6(self):
        from paperboy.scheduler import AirflowScheduler, DummyScheduler

    def test_import7(self):
        from paperboy.server.api import FalconAPI

    def test_import8(self):
        sys.modules['nbstripout'] = MagicMock()  # Doesnt work under nose
        from paperboy.storage import StorageEngine
        from paperboy.storage.dummy import NotebookDummyStorage, JobDummyStorage, ReportDummyStorage, UserDummyStorage
        from paperboy.storage.sqla import Base, JobSQLStorage, NotebookSQLStorage, ReportSQLStorage, UserSQLStorage

    # def test_import9(self):
    #     from paperboy.worker import *
