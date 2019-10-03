import sys
from datetime import datetime
from mongoengine import connect
from pymongo import MongoClient
from .models.user import UserMongo
from .models.notebook import NotebookMongo
from .models.job import JobMongo
from .models.report import ReportMongo


def main(mongo_url, db_name='paperboy'):
    '''Create dummy notebook data for sqlalchemy'''
    connect(db_name, host=mongo_url)
    user = UserMongo(name='test')
    user.save()

    notebook = '''
    '''
    created = datetime.now()
    modified = datetime.now()

    notebook = NotebookMongo(name='MyNotebook',
                             user=user,
                             notebook='',
                             privacy='',
                             level='',
                             requirements='',
                             dockerfile='',
                             created=created,
                             modified=modified)
    notebook.save()

    job = JobMongo(name='MyJob',
                   user=user,
                   notebook=notebook,
                   start_time=created,
                   interval='minutely',
                   level='production',
                   created=created,
                   modified=modified)
    job.save()

    type = 'run'
    output = 'notebook'
    strip_code = 'yes'

    created = datetime.now()
    modified = datetime.now()

    name = job.name + '-Report-1'

    param = '{}'
    report = ReportMongo(name=name,
                         user=user,
                         notebook=notebook,
                         job=job,
                         type=type,
                         output=output,
                         strip_code=strip_code,
                         parameters=param,
                         created=created,
                         modified=modified)
    report.save()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("args: <mongo_url>")
    else:
        main(sys.argv[1])
