from six import with_metaclass
from abc import abstractmethod, ABCMeta


class BaseOutput(with_metaclass(ABCMeta)):
    def __init__(self, config, *args, **kwargs):
        self.config = config

    @abstractmethod
    def write(self, report, *args, **kwargs):
        pass
