class BaseStorage(object):
    def __init__(self, config, *args, **kwargs):
        self.config = config


class NotebookStorage(BaseStorage):
    pass


class JobStorage(BaseStorage):
    pass


class ReportStorage(BaseStorage):
    pass
