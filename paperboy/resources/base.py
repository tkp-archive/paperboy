import logging


class BaseResource(object):
    '''Base falcon resource to handle shared attributes'''
    def __init__(self, config, db=None, scheduler=None):
        self.config = config
        self.db = db
        self.scheduler = scheduler
        self.logger = logging.getLogger('paperboy.' + __name__)
        self.session = None  # May be overridden by middleware
