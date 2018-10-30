import falcon
from six import with_metaclass
from abc import abstractmethod, ABCMeta


class BaseStorage(with_metaclass(ABCMeta)):
    def __init__(self, config, *args, **kwargs):
        self.config = config

    @abstractmethod
    def status(self, *args, **kwargs):
        pass

    @abstractmethod
    def form(self, req, resp, *args, **kwargs):
        pass

    @abstractmethod
    def search(self, count, id=None, name=None, session=None, *args, **kwargs):
        pass

    @abstractmethod
    def list(self, *args, **kwargs):
        pass

    @abstractmethod
    def detail(self, *args, **kwargs):
        pass

    @abstractmethod
    def store(self, req, resp, *args, **kwargs):
        pass


class UserStorage(BaseStorage):
    def __init__(self, config, *args, **kwargs):
        self.config = config

    @abstractmethod
    def login(self, context, *args, **kwargs):
        pass

    def logout(self, context, *args, **kwargs):
        return True


class NotebookStorage(BaseStorage):
    pass


class JobStorage(BaseStorage):
    pass


class ReportStorage(BaseStorage):
    @abstractmethod
    def generate(self, context, session, *args, **kwargs):
        pass
