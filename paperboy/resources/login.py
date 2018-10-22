import falcon
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
                                           include_password=self.config.include_password)
        resp.body = tpl

    def on_post(self, req, resp):
        username = req.get_param('username')
        resp.set_cookie('auth_token', username, max_age=60, path='/', secure=not self.config.http)  # FIXME unset false
        resp.status = falcon.HTTP_302
        resp.set_header('Location', self.config.baseurl)
