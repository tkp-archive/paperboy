from traitlets import HasTraits, Unicode, Bool
from ..storage.sqla import UserSQLStorage, NotebookSQLStorage, JobSQLStorage, ReportSQLStorage


class Storage(HasTraits):
    type = Unicode()
    user_storage = None
    notebook_storage = None
    job_storage = None
    report_storage = None


class SQLAStorage(Storage):
    type = 'SQLA'
    sql_url = Unicode(default_value='sqlite:///paperboy.db', help="SQL Alchemy url").tag(config=True)
    engine = None
    sessionmaker = None
    sql_user = Bool(default_value=True)

    user_storage = UserSQLStorage
    notebook_storage = NotebookSQLStorage
    job_storage = JobSQLStorage
    report_storage = ReportSQLStorage
