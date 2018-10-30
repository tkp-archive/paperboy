import falcon
import jinja2
from .base import BaseResource
from .html import read


class RegisterResource(BaseResource):
    auth_required = False

    def __init__(self, *args, **kwargs):
        super(RegisterResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        resp.content_type = 'text/html'
        file = read('register.html')
        tpl = jinja2.Template(file).render(baseurl=self.config.baseurl,
                                           apiurl=self.config.apiurl,
                                           registerurl=self.config.registerurl,
                                           include_password=self.config.include_password)
        resp.body = tpl

    def on_post(self, req, resp):
        req.context['params'] = req.params
        token = self.db.users.store(req.context, self.session)
        req.context['auth_token'] = token
        user = self.db.users.detail(req.context, self.session)

        if token and user:
            req.context['user'] = user
            resp.set_cookie('auth_token', token, max_age=self.config.token_timeout, path='/', secure=not self.config.http)
            resp.status = falcon.HTTP_302
            resp.set_header('Location', self.config.baseurl)
        else:
            resp.content_type = 'text/html'
            file = read('register.html')
            tpl = jinja2.Template(file).render(baseurl=self.config.baseurl,
                                               apiurl=self.config.apiurl,
                                               registerurl=self.config.registerurl,
                                               include_password=self.config.include_password)
            resp.body = tpl
