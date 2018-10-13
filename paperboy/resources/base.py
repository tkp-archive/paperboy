import logging


class BaseResource(object):
    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger('paperboy.' + __name__)
