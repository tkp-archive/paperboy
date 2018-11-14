from six import with_metaclass
from abc import abstractmethod, ABCMeta

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
    def __init__(self, config, db, *args, **kwargs):
        self.config = config
        self.db = db

    @abstractmethod
    def status(self, req, resp, *args, **kwargs):
        pass

    @abstractmethod
    def schedule(self, user, notebook, job, reports, *args, **kwargs):
        pass

    @abstractmethod
    def unschedule(self, user, notebook, job, reports, *args, **kwargs):
        pass
