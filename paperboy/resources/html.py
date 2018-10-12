import falcon
import os
import os.path
import mimetypes
import jinja2
from functools import lru_cache


# @lru_cache(20)
def read(file):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'templates', file))
    if not os.path.exists(path):
        return None
    with open(path, 'r') as fp:
        return fp.read()


class HTMLResource(object):
    def on_get(self, req, resp):
        if req.path == '' or req.path == '/':
            path = 'index.html'
        else:
            path = req.path

        filetype = mimetypes.guess_type(path, strict=True)[0]
        resp.content_type = filetype

        file = read(path)
        if file:
            tpl = jinja2.Template(file).render()
            resp.body = tpl
        else:
            resp.status = falcon.HTTP_404
