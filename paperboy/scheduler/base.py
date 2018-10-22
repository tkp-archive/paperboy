from six import with_metaclass
from abc import abstractmethod, ABCMeta


class BaseScheduler(with_metaclass(ABCMeta)):
    def __init__(self, config, db, *args, **kwargs):
        self.config = config
        self.db = db

    @abstractmethod
    def status(self, req, resp):
        pass
