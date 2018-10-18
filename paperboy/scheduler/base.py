from six import with_metaclass
from abc import abstractmethod, ABCMeta


class BaseScheduler(with_metaclass(ABCMeta)):
    def __init__(self, config, *args):
        self.config = config

    @abstractmethod
    def status(self, req, resp):
        pass
