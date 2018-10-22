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
        self.db.users.store(req, resp)
