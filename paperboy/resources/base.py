import logging


class BaseResource(object):
    def __init__(self, config, db=None):
        self.config = config
        self.db = db
        self.logger = logging.getLogger('paperboy.' + __name__)
