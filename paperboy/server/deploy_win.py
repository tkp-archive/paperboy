from waitress import serve


class FalconWaitress():
    def __init__(self, app, options=None):
        self.application = app
        self.host, self.port = options.get('bind', '0.0.0.0:8080').split(':')
        self.workers = options.get('workers', 1)
        super(FalconWaitress, self).__init__()

    def run(self):
        serve(self.application, host=self.host, port=self.port, threads=self.workers)
