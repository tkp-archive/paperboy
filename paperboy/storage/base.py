import falcon
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

    def _do_login(self, token, req, resp):
        resp.set_cookie('auth_token', token, max_age=self.config.token_timeout, path='/', secure=not self.config.http)
        resp.status = falcon.HTTP_302
        resp.set_header('Location', self.config.baseurl)

    def logout(self, req, resp):
        resp.unset_cookie('auth_token')
        resp.status = falcon.HTTP_302
        resp.set_header('Location', self.config.baseurl)


class NotebookStorage(BaseStorage):
    pass


class JobStorage(BaseStorage):
    pass


class ReportStorage(BaseStorage):
    pass
