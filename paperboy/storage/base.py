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
    def list(self, req, resp, *args, **kwargs):
        pass

    @abstractmethod
    def detail(self, req, resp, *args, **kwargs):
        pass

    @abstractmethod
    def store(self, req, resp, *args, **kwargs):
        pass


class UserStorage(BaseStorage):
    def __init__(self, config, *args, **kwargs):
        self.config = config

    @abstractmethod
    def login(self, req, resp, *args, **kwargs):
        pass

    def _do_login(self, token, req, resp, *args, **kwargs):
        resp.set_cookie('auth_token', token, max_age=self.config.token_timeout, path='/', secure=not self.config.http)
        resp.status = falcon.HTTP_302
        resp.set_header('Location', self.config.baseurl)

    def logout(self, req, resp, *args, **kwargs):
        resp.unset_cookie('auth_token')
        resp.status = falcon.HTTP_302
        resp.set_header('Location', self.config.baseurl)


class NotebookStorage(BaseStorage):
    pass


class JobStorage(BaseStorage):
    pass


class ReportStorage(BaseStorage):
    @abstractmethod
    def autogenerate(self, req, resp, session, *args, **kwargs):
        pass
