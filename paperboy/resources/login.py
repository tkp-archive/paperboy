import jinja2
from .base import BaseResource
from .html import read


class LoginResource(BaseResource):
    auth_required = False

    def __init__(self, *args, **kwargs):
        super(LoginResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        resp.content_type = 'text/html'
        file = read('login.html')
        tpl = jinja2.Template(file).render(baseurl=self.config.baseurl,
                                           apiurl=self.config.apiurl,
                                           loginurl=self.config.loginurl,
                                           include_register=self.config.include_register,
                                           registerurl=self.config.registerurl,
                                           include_password=self.config.include_password)
        resp.body = tpl

    def on_post(self, req, resp):
        self.db.users.login(req, resp, session=getattr(self, 'session', None))
        if req.context.get('auth_token') is None:
            resp.content_type = 'text/html'
            file = read('login.html')
            tpl = jinja2.Template(file).render(baseurl=self.config.baseurl,
                                               apiurl=self.config.apiurl,
                                               loginurl=self.config.loginurl,
                                               include_register=self.config.include_register,
                                               registerurl=self.config.registerurl,
                                               include_password=self.config.include_password)
            resp.body = tpl
