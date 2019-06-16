import logging
import math
from mongoengine.queryset.visitor import Q
from paperboy.config import ListResult
from .models.user import UserMongo


class BaseMongoStorageMixin(object):
    '''Base class to share common MongoDB operations between User/Notebook/Job/Report backends'''

    def _form(self, ConfigCls):
        '''Generate form from configuration type.

        Args:
            ConfigCls (paperboy.config.base.Base): UserConfig/NotebookConfig/JobConfig/ReportConfig
        Returns:
            paperboy.config.forms.Response
        '''
        return ConfigCls(self.config).form()

    def _search(self, MongoCls, ClsName, user, params, session, *args, **kwargs):
        '''Search for a given name in instances of ClsName stored in Mongo as type MongoCls

        Args:
            MongoCls (BaseMongoStorageMixin + BaseStorage): Class implementing the BaseStorage interface
            ClsName (string): Notebook/Job/Report
            user (paperboy.storage.base.UserStorage): the user access this data
            params (dict): query parameters
            session (mongodb session): the active mongodb session
        Returns:
            list: results with name/id
        '''
        user = UserMongo.objects(id=user.id).first()
        name = params.get('name', '')
        count = int(params.get('count', 10))
        if name is None or name == '':
            return []
        q = Q(name=name)
        q |= Q(user=user)
        if hasattr(MongoCls, 'privacy'):
            q |= Q(privacy='public')
        nbs = MongoCls.objects(q).limit(count)

        return [{'id': ClsName + '-' + str(nb.id), 'name': nb.name} for nb in nbs]

    def _list(self, MongoCls, setter, user, params, session, *args, **kwargs):
        '''List all instances of a give storage class

        Args:
            MongoCls (BaseMongoStorageMixin + BaseStorage): Class implementing the BaseStorage interface
            setter (string): unused
            user (paperboy.storage.base.UserStorage): the user access this data
            params (dict): query parameters
            session (mongodb session): the active mongodb session
        Returns:
            list of paperboy.config.base.Base: result notebooks/jobs/reports as json
        '''
        user = UserMongo.objects(id=user.id).first()
        q = Q(user=user)
        if hasattr(MongoCls, 'privacy'):
            q |= Q(privacy='public')
        base = MongoCls.objects(q)
        page = int(params.get('page', 1))
        nbs = base[25*(page-1):25*page]

        result = ListResult()
        result.total = base.count()
        result.count = len(nbs)
        result.page = page
        result.pages = math.ceil(result.total/25) if result.count > 0 else 1

        logging.critical('list : {}, result : {} - {}'.format(MongoCls, result.total, len(nbs)))

        result.results = [x.to_config(self.config) for x in nbs]
        return result.to_json()

    def _detail(self, MongoCls, user, params, session, *args, **kwargs):
        '''Get detailed view of instance

        Args:
            MongoCls (BaseMongoStorageMixin + BaseStorage): Class implementing the BaseStorage interface
            user (paperboy.storage.base.UserStorage): the user access this data
            params (dict): query parameters
            session (mongodb session): the active mongodb session
        Returns:
            edit of paperboy.config.base.Base: notebook/job/report config edit
        '''
        id = justid(params.get('id') or -1)
        try:
            id = int(id)
        except ValueError:
            return {}

        if id < 0:
            return {}

        nb_mdb = MongoCls.objects(id=id)  # FIXME permission?

        logging.critical('detail : {}, result : {}'.format(id, nb_mdb))

        if nb_mdb:
            return nb_mdb.to_config(self.config).edit()
        return {}


def justid(id):
    '''Helper method to turn name-id string into just id'''
    if isinstance(id, int):
        return id
    if '-' in id:
        return id.split('-', 1)[-1]
    return id
