from datetime import datetime
from sqlalchemy import create_engine
from .models.user import UserMongo
from .models.notebook import NotebookMongo
from .models.job import JobMongo
from .models.report import ReportMongo


def main(sql_url):
    '''Create dummy notebook data for sqlalchemy'''
    engine = create_engine(sql_url, echo=False)
    with engine.session() as session:
        user = UserMongo(name='test')
        session.add(user)
        session.commit()
        session.refresh(user)

        notebook = '''
        '''
        created = datetime.now()
        modified = datetime.now()

        notebook = NotebookMongo(name='MyNotebook',
                                 userId=user.id,
                                 user=user,
                                 notebook='',
                                 privacy='',
                                 level='',
                                 requirements='',
                                 dockerfile='',
                                 created=created,
                                 modified=modified)
        session.add(notebook)
        session.commit()
        session.refresh(notebook)

        job = JobMongo(name='MyJob',
                       userId=user.id,
                       user=user,
                       notebookId=notebook.id,
                       notebook=notebook,
                       start_time=created,
                       interval='minutely',
                       level='production',
                       created=created,
                       modified=modified)
        session.add(job)
        session.commit()
        session.refresh(job)

        type = 'run'
        output = 'notebook'
        strip_code = 'yes'

        created = datetime.now()
        modified = datetime.now()

        name = job.name + '-Report-1'

        param = '{}'
        report = ReportMongo(name=name,
                             userId=user.id,
                             user=user,
                             notebookId=notebook.id,
                             notebook=notebook,
                             jobId=job.id,
                             job=job,
                             type=type,
                             output=output,
                             strip_code=strip_code,
                             parameters=param,
                             created=created,
                             modified=modified)
        session.add(report)
        session.commit()
        session.refresh(report)
