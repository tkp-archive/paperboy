from six.moves.urllib_parse import urljoin
from datetime import datetime
from traitlets import HasTraits, Unicode, Int, Instance
from .forms import Form, FormEntry, DOMEntry
from .base import Base


class NotebookMetadata(HasTraits):
    username = Unicode()
    userid = Unicode()

    notebook = Unicode()
    privacy = Unicode()
    sla = Unicode()
    requirements = Unicode(allow_none=True)
    dockerfile = Unicode(allow_none=True)

    jobs = Int()
    reports = Int()

    created = Instance(datetime)
    modified = Instance(datetime)

    def to_json(self):
        ret = {}
        ret['username'] = self.username
        ret['userid'] = self.userid
        ret['notebook'] = self.notebook

        if self.privacy:
            ret['privacy'] = self.privacy
        if self.sla:
            ret['sla'] = self.sla
        if self.jobs:
            ret['jobs'] = self.jobs
        if self.reports:
            ret['reports'] = self.reports
        if self.created:
            ret['created'] = self.created.strftime('%m/%d/%Y %H:%M:%S')
        if self.modified:
            ret['modified'] = self.modified.strftime('%m/%d/%Y %H:%M:%S')

        return ret

    @staticmethod
    def from_json(jsn):
        ret = NotebookMetadata()
        for k, v in jsn.items():
            if k in ('created', 'modified'):
                ret.set_trait(k, datetime.strptime(v, '%m/%d/%Y %H:%M:%S'))
            else:
                ret.set_trait(k, v)
        return ret


class Notebook(Base):
    name = Unicode()
    id = Unicode()
    meta = Instance(NotebookMetadata)

    def to_json(self):
        ret = {}
        ret['name'] = self.name
        ret['id'] = self.id
        ret['meta'] = self.meta.to_json()
        return ret

    def form(self):
        f = Form()
        f.entries = [
            FormEntry(name='file', type='file', label='File', required=True),
            FormEntry(name='name', type='text', label='Name', placeholder='Name for Notebook...', required=True),
            FormEntry(name='privacy', type='select', label='Privacy', options=['Private', 'Public'], required=True),
            FormEntry(name='sla', type='select', label='SLA', options=['Production', 'Research', 'Development', 'Personal'], required=True),
            FormEntry(name='build', type='label', label='Build options'),
            FormEntry(name='requirements', type='file', label='requirements.txt', required=False),
            FormEntry(name='dockerfile', type='file', label='Dockerfile', required=False),
            FormEntry(name='submit', type='submit', value='Create', url=urljoin(self.config.apiurl, 'notebooks')),
        ]
        return f.to_json()

    @staticmethod
    def from_json(jsn, config):
        ret = Notebook(config)
        ret.name = jsn.pop('name')
        ret.id = jsn.pop('id')

        if 'meta' in jsn:
            ret.meta = NotebookMetadata.from_json(jsn['meta'])
        else:
            ret.meta = NotebookMetadata.from_json(jsn)

        return ret

    def edit(self):
        f = Form()
        f.entries = [
            FormEntry(name='name', type='text', value=self.name, placeholder='Name for Job...', required=True),
            FormEntry(name='privacy', type='select', value=self.meta.privacy, label='Visibility', options=['Private', 'Public'], required=True),
            FormEntry(name='sla', type='select', value=self.meta.sla, label='SLA', options=['Production', 'Research', 'Development', 'Personal'], required=True),
            FormEntry(name='notebook', type='json', value=self.meta.notebook, placeholder='Notebook json...', required=True)
        ]
        if self.meta.requirements:
            f.entries.append(FormEntry(name='requirements', type='textarea', value=self.meta.requirements, label='requirements.txt', required=False))
        if self.meta.dockerfile:
            f.entries.append(FormEntry(name='dockerfile', type='textarea', value=self.meta.dockerfile, label='Dockerfile', required=False))

        f.entries.append(FormEntry(name='save', type='submit', value='save', url=urljoin(self.config.apiurl, 'notebooks')))
        return f.to_json()

    def store(self):
        ret = []
        ret.append(DOMEntry(type='p', value='Success!').to_json())
        ret.append(DOMEntry(type='p', value='Successfully stored notebook: {}'.format(self.name)).to_json())
        return ret
