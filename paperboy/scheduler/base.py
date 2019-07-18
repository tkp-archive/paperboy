from six import with_metaclass
from abc import abstractmethod, ABCMeta
from random import choice

# Approximate string->cron/airflow intervals
TIMING_MAP = {
  'minutely': '*/1 * * * *',
  '5 minutes': '*/5 * * * *',
  '10 minutes': '*/10 * * * *',
  '30 minutes': '*/30 * * * *',
  'hourly': '@hourly',
  '2 hours': '0 */2 * * *',
  '3 hours': '0 */3 * * *',
  '6 hours': '0 */6 * * *',
  '12 hours': '0 */12 * * *',
  'daily': '@daily',
  'weekly': '@weekly',
  'monthly': '@monthly'
}


class BaseScheduler(with_metaclass(ABCMeta)):
    '''Scheduler abstract base class'''

    def __init__(self, config, db, *args, **kwargs):
        self.config = config
        self.db = db

    @abstractmethod
    def status(self, req, resp, *args, **kwargs):
        '''Get status for a given request
        Args:
            req (falcon Request)
            resp (falcon response)
        '''
        pass

    @abstractmethod
    def schedule(self, user, notebook, job, reports, *args, **kwargs):
        '''Schedule a job to generate reports for notebook and user
        Args:
            user (paperboy.config.User): user requesting the scheduling
            notebook (paperboy.config.Notebook): Notebook for the job
            job (paperboy.config.Job): Job parameters
            reports ([paperboy.config.Report]): Report configurations with parameters
        '''
        pass

    @abstractmethod
    def unschedule(self, user, notebook, job, reports, *args, **kwargs):
        '''Unschedule a job to generate reports for notebook and user
        Args:
            user (paperboy.config.User): user requesting the scheduling
            notebook (paperboy.config.Notebook): Notebook for the job
            job (paperboy.config.Job): Job parameters
            reports ([paperboy.config.Report]): Report configurations with parameters
        '''
        pass


class DummyScheduler(BaseScheduler):
    '''Dummy Scheduler class'''

    def __init__(self, config, db, *args, **kwargs):
        self.config = config
        self.db = db

    def status(self, user, params, session, *args, **kwargs):
        '''Get status for a given request
        Args:
            req (falcon Request)
            resp (falcon response)
        '''
        type = params.get('type', '')
        gen = DummyScheduler.fakequery()
        if type == 'jobs':
            return gen['jobs']
        elif type == 'reports':
            return gen['reports']
        else:
            return gen

    @staticmethod
    def fakequery():
        '''If airflow not present, fake the results for now so the UI looks ok'''
        ret = {'jobs': [], 'reports': []}
        for i in range(10):
            ret['jobs'].append(
                {'name': 'DAG-Job-{}'.format(i),
                 'id': 'Job-{}'.format(i),
                 'meta': {
                    'id':  'Job-{}'.format(i),
                    'execution': '01/02/2018 12:25:31',
                    'status': choice(['✔', '✘'])}
                 }
            )
            ret['reports'].append(
                {'name': 'Report-{}'.format(i),
                 'id': 'Report-{}'.format(i),
                 'meta': {
                    'run': '01/02/2018 12:25:31',
                    'status': choice(['✔', '✘']),
                    'type': choice(['Post', 'Papermill', 'NBConvert', 'Setup']),
                    }
                 }
            )
        return ret

    def schedule(self, user, notebook, job, reports, *args, **kwargs):
        '''Schedule a job to generate reports for notebook and user
        Args:
            user (paperboy.config.User): user requesting the scheduling
            notebook (paperboy.config.Notebook): Notebook for the job
            job (paperboy.config.Job): Job parameters
            reports ([paperboy.config.Report]): Report configurations with parameters
        '''
        pass

    def unschedule(self, user, notebook, job, reports, *args, **kwargs):
        '''Unschedule a job to generate reports for notebook and user
        Args:
            user (paperboy.config.User): user requesting the scheduling
            notebook (paperboy.config.Notebook): Notebook for the job
            job (paperboy.config.Job): Job parameters
            reports ([paperboy.config.Report]): Report configurations with parameters
        '''
        pass
