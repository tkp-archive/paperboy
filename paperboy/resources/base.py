import logging


class BaseResource(object):
    def __init__(self, config, db=None, scheduler=None):
        self.config = config
        self.db = db
        self.scheduler = scheduler
        self.logger = logging.getLogger('paperboy.' + __name__)
