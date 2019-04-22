import falcon
import jinja2
from .base import BaseResource
from .html import read


class LoginResource(BaseResource):
    '''Falcon resource for user authentication'''

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
        token = self.db.users.login(None, req.params, self.session)
        user = self.db.users.detail(token, req.params, self.session)

        if token and user:
            req.context['auth_token'] = token
            req.context['user'] = user
            resp.set_cookie('auth_token', token, max_age=self.config.token_timeout, path='/', secure=not self.config.http)
            resp.status = falcon.HTTP_302
            resp.set_header('Location', self.config.baseurl)

        else:
            resp.content_type = 'text/html'
            file = read('login.html')
            tpl = jinja2.Template(file).render(baseurl=self.config.baseurl,
                                               apiurl=self.config.apiurl,
                                               loginurl=self.config.loginurl,
                                               include_register=self.config.include_register,
                                               registerurl=self.config.registerurl,
                                               include_password=self.config.include_password)
            resp.body = tpl
