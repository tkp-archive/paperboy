from traitlets import HasTraits, Unicode, Bool, Type
from ..storage.sqla import UserSQLStorage, NotebookSQLStorage, JobSQLStorage, ReportSQLStorage
from ..storage.mongo import UserMongoStorage, NotebookMongoStorage, JobMongoStorage, ReportMongoStorage


class StorageConfig(HasTraits):
    '''Base config for storage backend'''
    type = Unicode()
    user_storage = None
    notebook_storage = None
    job_storage = None
    report_storage = None


class SQLAStorageConfig(StorageConfig):
    '''Config for SQL Alchemy storage'''
    type = 'SQLA'
    sql_url = Unicode(default_value='sqlite:///paperboy.db', help="SQL Alchemy url").tag(config=True)
    engine = None
    sessionmaker = None
    sql_user = Bool(default_value=True)

    user_storage = Type(klass=UserSQLStorage)
    notebook_storage = Type(klass=NotebookSQLStorage)
    job_storage = Type(klass=JobSQLStorage)
    report_storage = Type(klass=ReportSQLStorage)


class MongoStorageConfig(StorageConfig):
    '''Config for SQL Alchemy storage'''
    type = 'Mongo'
    mongo_url = Unicode(default_value='mongodb://localhost:27017/', help="MongoDB url").tag(config=True)
    db_name = Unicode(default_value='paperboy')

    user_storage = Type(klass=UserMongoStorage)
    notebook_storage = Type(klass=NotebookMongoStorage)
    job_storage = Type(klass=JobMongoStorage)
    report_storage = Type(klass=ReportMongoStorage)
