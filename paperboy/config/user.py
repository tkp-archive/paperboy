from six.moves.urllib_parse import urljoin
from traitlets import Unicode
from .forms import Form, FormEntry, DOMEntry
from .base import Base


class User(Base):
    name = Unicode()
    id = Unicode()

    def to_json(self):
        ret = {}
        ret['name'] = self.name
        ret['id'] = self.id
        return ret

    def form(self):
        f = Form()
        f.entries = [
            FormEntry(name='name', type='text', label='Name', placeholder='Name for Notebook...', required=True),
            FormEntry(name='submit', type='submit', value='Create', url=urljoin(self.config.apiurl, 'notebooks')),
        ]
        return f.to_json()

    @staticmethod
    def from_json(jsn, config):
        ret = User(config)
        ret.name = jsn.pop('name')
        ret.id = jsn.pop('id')
        return ret

    def edit(self):
        f = Form()
        f.entries = [
            FormEntry(name='name', type='text', value=self.name, placeholder='Name for Job...', required=True),
            FormEntry(name='save', type='submit', value='save', url=urljoin(self.config.apiurl, 'notebooks'))
        ]
        return f.to_json()

    def store(self):
        ret = []
        ret.append(DOMEntry(type='p', value='Success!').to_json())
        ret.append(DOMEntry(type='p', value='Successfully stored user {}'.format(self.name)).to_json())
        return ret
