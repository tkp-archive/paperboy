import json
import nbformat
import logging
from random import randint, choice
from paperboy.config import Notebook
from paperboy.config.storage import NotebookListResult
from paperboy.storage import NotebookStorage


class NotebookDummyStorage(NotebookStorage):
    def form(self):
        return Notebook(self.config).form()

    def list(self, req, resp):
        resp.content_type = 'application/json'
        result = NotebookListResult()
        result.page = 1
        result.pages = 1
        result.count = 25
        result.total = 25
        result.notebooks = [
            Notebook.from_json(
                {'name': 'TestNB%d' % i,
                 'id': 'Notebook-%d' % i,
                 'meta': {
                     'author': 'Test Author',
                     'visibility': choice(['public'] * 10 + ['private']),
                     'jobs': randint(1, 100),
                     'reports': randint(1, 1000),
                     'created': '10/14/2018 04:50:33',
                     'modified': '10/14/2018 18:25:31'}},
                self.config)
            for i in range(25)]
        resp.body = result.to_json(True)

    def detail(self, req, resp):
        resp.content_type = 'application/json'
        details =Notebook.from_json(dict(name='MyNotebook', id='Notebook-1', author='Joe Python', jobs=25, reports=353, created='10/14/2018 04:50:33', modified='10/14/2018 18:25:31'), self.config).edit()
        resp.body = json.dumps(details)

    def store(self, req, resp):
        name = req.get_param('name')
        nb = nbformat.reads(req.get_param('file').file.read(), 4)
        resp.content_type = 'application/json'
        store = Notebook.from_json(dict(name='MyNotebook', id='Notebook-1', author='Joe Python', jobs=25, reports=353, created='10/14/2018 04:50:33', modified='10/14/2018 18:25:31'), self.config).store()
        logging.critical("Storing notebook {}".format(name))
        resp.body = json.dumps(store)
