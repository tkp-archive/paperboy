import jinja2
from .base import BaseResource
from .html import read


class LogoutResource(BaseResource):
    auth_required = False

    def __init__(self, *args, **kwargs):
        super(LogoutResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        resp.content_type = 'text/html'
        file = read('logout.html')
        tpl = jinja2.Template(file).render(baseurl=self.config.baseurl,
                                           apiurl=self.config.apiurl,
                                           loginurl=self.config.loginurl,
                                           logouturl=self.config.logouturl)
        resp.body = tpl

    def on_post(self, req, resp):
        self.db.users.login(req, resp)
