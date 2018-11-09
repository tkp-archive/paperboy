import logging
from sqlalchemy import or_
from paperboy.config import ListResult


class BaseSQLStorageMixin(object):
    def _form(self, ConfigCls):
        return ConfigCls(self.config).form()

    def _search(self, SqlCls, ClsName, user, params, session, *args, **kwargs):
        name = params.get('name', '')
        count = int(params.get('count', 10))
        if name is None or name == '':
            return []
        nbs = session.query(SqlCls) \
            .filter(SqlCls.name.like(lookfor(name))) \
            .filter(SqlCls.userId == int(user.id) or
                    (hasattr(SqlCls, 'privacy') and SqlCls.privacy == 'public')) \
            .limit(count)

        return [{'id': ClsName + '-' + str(nb.id), 'name': nb.name} for nb in nbs]

    def _list(self, SqlCls, setter, user, params, session, *args, **kwargs):
        base = session.query(SqlCls) \
                .filter(or_(SqlCls.userId.like((user.id)),
                        (hasattr(SqlCls, 'privacy') and SqlCls.privacy == 'public'))) \

        result = ListResult()
        result.total = base.count()

        result.count = min(result.total, 25)
        result.page = 1
        result.pages = int(result.total/result.count) if result.count > 0 else 1

        nbs = base.limit(25).all()

        logging.critical('list : {}, result : {} - {}'.format(SqlCls, result.total, len(nbs)))

        result.results = [x.to_config(self.config) for x in nbs]
        return result.to_json()

    def _detail(self, SqlCls, user, params, session, *args, **kwargs):
        id = justid(params.get('id') or -1)
        try:
            id = int(id)
        except ValueError:
            return {}

        if id < 0:
            return {}

        nb_sql = session.query(SqlCls) \
            .filter(SqlCls.userId == int(user.id) or
                    (hasattr(SqlCls, 'privacy') and SqlCls.privacy == 'public')) \
            .get(id)

        logging.critical('detail : {}, result : {}'.format(id, nb_sql))

        if nb_sql:
            return nb_sql.to_config(self.config).edit()
        return {}


def lookfor(s):
    if '*' in s or '_' in s:
        return s.replace('_', '__')\
                .replace('*', '%')\
                .replace('?', '_')
    return '%{0}%'.format(s)


def justid(id):
    if isinstance(id, int):
        return id
    if '-' in id:
        return id.split('-', 1)[-1]
    return id
