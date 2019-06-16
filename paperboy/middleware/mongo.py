from pymongo import MongoClient


class MongoSessionMiddleware(object):
    '''variant of https://gitlab.com/skosh/falcon-helpers/blob/master/falcon_helpers/middlewares/sqla.py'''
    def __init__(self, db_url, db_name):
        print(db_url)
        print(db_name)
        self.db_url = db_url
        self.db_name = db_name

    def process_resource(self, req, resp, resource, params):
        '''initialize SQL Alchemy session and put into resource's `session` variable'''
        resource.session = MongoClient(self.db_url)[self.db_name]

    def process_response(self, req, resp, resource, req_succeeded):
        '''If session is successful, commit, otherwise revert'''
        pass
