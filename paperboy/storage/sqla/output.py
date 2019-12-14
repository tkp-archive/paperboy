import logging
from datetime import datetime
from paperboy.config import OutputConfig
from paperboy.storage import OutputStorage
from .base import BaseSQLStorageMixin, justid
from .models.report import ReportSQL
from .models.output import OutputSQL


class OutputSQLStorage(BaseSQLStorageMixin, OutputStorage):
    def status(self, user, params, session, *args, **kwargs):
        base = session.query(OutputSQL) \
            .filter(OutputSQL.userId == int(user.id))
        return {'total': base.count()}

    def form(self):
        '''Pass through to shared method in BaseSQLStorageMixin'''
        return self._form(OutputConfig)

    def search(self, user, params, session, *args, **kwargs):
        '''Pass through to shared method in BaseSQLStorageMixin'''
        return self._search(OutputSQL, 'Output', user, params, session, *args, **kwargs)

    def list(self, user, params, session, *args, **kwargs):
        '''Pass through to shared method in BaseSQLStorageMixin'''
        return self._list(OutputSQL, 'outputs', user, params, session, *args, **kwargs)

    def detail(self, user, params, session, *args, **kwargs):
        '''Pass through to shared method in BaseSQLStorageMixin'''
        return self._detail(OutputSQL, user, params, session, *args, **kwargs)

    def store(self, user, params, session, *args, **kwargs):
        name = params.get('name')
        reportid = params.get('report')
        data = params.get('data')
        report = session.query(ReportSQL).get(int(justid(reportid)))

        created = datetime.now()

        op = OutputSQL(name=name,
                       reportId=reportid,
                       report=report,
                       created=created,
                       data=data)

        session.add(op)

        # generate id
        session.flush()
        session.refresh(op)

        store = op.to_config(self.config).store()
        logging.critical("Storing output {}".format(op))
        return store

    def delete(self, user, params, session, *args, **kwargs):
        # TODO only if allowed
        id = justid(params.get('id'))
        op = session.query(OutputSQL).filter(OutputSQL.id == id).first()
        session.delete(op)
        return [{"name": "", "type": "p", "value": "Success!", "required": False, "readonly": False, "hidden": False},
                {"name": "", "type": "p", "value": "Successfully deleted output: " + id, "required": False, "readonly": False, "hidden": False}]
