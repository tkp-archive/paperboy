from six.moves.urllib_parse import urljoin
from traitlets import Unicode
from .forms import Response, FormEntry, DOMEntry
from .base import Base


class UserConfig(Base):
    name = Unicode()
    id = Unicode()

    def to_json(self):
        ret = {}
        ret['name'] = self.name
        ret['id'] = self.id
        return ret

    def form(self):
        f = Response()
        f.entries = [
            FormEntry(name='name', type='text', label='Name', placeholder='Name for Notebook...', required=True),
            FormEntry(name='submit', type='submit', value='save', url=urljoin(self.config.apiurl, 'users?action=save')),
        ]
        return f.to_json()

    @staticmethod
    def from_json(jsn, config):
        ret = UserConfig(config)
        ret.name = jsn.pop('name')
        ret.id = jsn.pop('id')
        return ret

    def edit(self):
        f = Response()
        f.entries = [
            FormEntry(name='name', type='text', value=self.name, placeholder='Name for Job...', required=True),
            FormEntry(name='save', type='submit', value='save', url=urljoin(self.config.apiurl, 'users?action=save'))
        ]
        return f.to_json()

    def store(self):
        ret = Response()
        ret.entries = [
            DOMEntry(type='p', value='Success!'),
            DOMEntry(type='p', value='Successfully stored user {}'.format(self.name)),
        ]
        return ret
