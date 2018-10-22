from six import with_metaclass
from abc import abstractmethod, ABCMeta


class BaseStorage(with_metaclass(ABCMeta)):
    def __init__(self, config, *args, **kwargs):
        self.config = config

    @abstractmethod
    def form(self, req, resp):
        pass

    @abstractmethod
    def list(self, req, resp):
        pass

    @abstractmethod
    def detail(self, req, resp):
        pass

    @abstractmethod
    def store(self, req, resp):
        pass


class UserStorage(BaseStorage):
    def __init__(self, config, *args, **kwargs):
        self.config = config

    @abstractmethod
    def login(self, req, resp):
        pass

    @abstractmethod
    def logout(self, req, resp):
        pass


class NotebookStorage(BaseStorage):
    pass


class JobStorage(BaseStorage):
    pass


class ReportStorage(BaseStorage):
    pass
