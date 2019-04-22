from six import with_metaclass
from abc import abstractmethod, ABCMeta

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
