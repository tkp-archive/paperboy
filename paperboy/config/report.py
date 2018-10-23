import json
from six.moves.urllib_parse import urljoin
from datetime import datetime
from traitlets import HasTraits, Unicode, Instance, Bool
from .forms import Form, FormEntry, DOMEntry
from .base import Base
from .notebook import Notebook
from .job import Job


class ReportMetadata(HasTraits):
    notebook = Instance(Notebook)
    job = Instance(Job)
    created = Instance(datetime)

    username = Unicode()
    userid = Unicode()

    run = Instance(datetime)
    params = Unicode()
    type = Unicode()
    output = Unicode()
    strip_code = Bool()

    def to_json(self, string=False):
        ret = {}
        ret = {}
        ret['notebook'] = self.notebook.name
        ret['notebookid'] = self.notebook.id
        ret['job'] = self.job.name
        ret['jobid'] = self.job.id

        if self.created:
            ret['created'] = self.created.strftime('%m/%d/%Y %H:%M:%S')

        if self.run:
            ret['run'] = self.run.strftime('%m/%d/%Y %H:%M:%S')

        if string:
            return json.dumps(ret)
        return ret

    @staticmethod
    def from_json(jsn, string=False):
        ret = ReportMetadata()
        if string:
            jsn = json.loads(jsn)
        for k, v in jsn.items():
            if k in ('created', 'run'):
                ret.set_trait(k, datetime.strptime(v, '%m/%d/%Y %H:%M:%S'))
            else:
                ret.set_trait(k, v)
        return ret


class Report(Base):
    name = Unicode()
    id = Unicode()
    meta = Instance(ReportMetadata)

    def to_json(self, string=False):
        ret = {}
        ret['name'] = self.name
        ret['id'] = self.id
        ret['meta'] = self.meta.to_json()
        if string:
            return json.dumps(ret)
        return ret

    def form(self, string=False):
        f = Form()
        f.entries = [
            FormEntry(name='name', type='text', label='Name', placeholder='Name for Report...', required=True),
            FormEntry(name='notebook', type='autocomplete', label='Notebook', url=urljoin(self.config.apiurl, 'autocomplete?type=notebooks&partial='), required=True),
            FormEntry(name='job', type='autocomplete', label='Job', url=urljoin(self.config.apiurl, 'autocomplete?type=jobs&partial='), required=True),
            FormEntry(name='params', type='textarea', label='Parameters', placeholder='JSON Parameters...'),
            FormEntry(name='type', type='select', label='Type', options=['Run', 'Publish'], required=True),
            FormEntry(name='output', type='select', label='Output', options=['Email', 'PDF', 'HTML', 'Script'], required=True),
            FormEntry(name='code', type='select', label='Strip Code', options=['Yes', 'No'], required=True),
            FormEntry(name='submit', type='submit', value='Create', url=urljoin(self.config.apiurl, 'reports'))
        ]
        if string:
            return f.to_json(string)
        return f.to_json()

    @staticmethod
    def from_json(jsn, config, string=False):
        ret = Report(config)
        if string:
            jsn = json.loads(jsn)
        ret.name = jsn['name']
        ret.id = jsn['id']
        ret.meta = ReportMetadata.from_json(jsn['meta'])
        ret.meta.notebook = Notebook(config)  # FIXME
        ret.meta.job = Job(config)  # FIXME
        return ret

    def edit(self):
        f = Form()
        f.entries = [
            FormEntry(name='name', type='text', label='Name', value=self.name, placeholder='Name for Report...', required=True),
            FormEntry(name='notebook', type='autocomplete', label='Notebook', url=urljoin(self.config.apiurl, 'autocomplete?type=notebooks&partial='), required=True),
            FormEntry(name='job', type='autocomplete', label='Job', url=urljoin(self.config.apiurl, 'autocomplete?type=jobs&partial='), required=True),
            FormEntry(name='params', type='textarea', label='Parameters', placeholder='JSON Parameters...'),
            FormEntry(name='type', type='select', label='Type', options=['Run', 'Publish'], required=True),
            FormEntry(name='output', type='select', label='Output', options=['Email', 'PDF', 'HTML', 'Script'], required=True),
            FormEntry(name='code', type='select', label='Strip Code', options=['Yes', 'No'], required=True),
            FormEntry(name='save', type='submit', value='save', url=urljoin(self.config.apiurl, 'jobs'))
        ]
        return f.to_json()

    def store(self):
        ret = []
        ret.append(DOMEntry(type='h2', value='Success!').to_json())
        ret.append(DOMEntry(type='p', value='Successfully configured job 1!').to_json())
        ret.append(DOMEntry(type='p', value='Notebook: {}'.format('')).to_json())
        return ret
