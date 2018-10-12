class TestResource(object):
    def on_get(self, req, resp):
        resp.body = 'Hello, world!'
