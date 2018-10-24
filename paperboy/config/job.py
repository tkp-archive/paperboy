from six.moves.urllib_parse import urljoin
from datetime import datetime
from traitlets import HasTraits, Unicode, Int, Instance, validate, TraitError
from .forms import Form, FormEntry, DOMEntry
from .base import Base, _INTERVAL_TYPES, _OUTPUT_TYPES, _REPORT_TYPES, _SERVICE_LEVELS
from .notebook import Notebook


class JobMetadata(HasTraits):
    notebook = Instance(Notebook)
    username = Unicode()
    userid = Unicode()

    start_time = Instance(datetime)
    interval = Unicode()
    level = Unicode()

    @validate('interval')
    def _validate_interval(self, proposal):
        if proposal['value'] not in _INTERVAL_TYPES:
            raise TraitError('Unrecognized type : {}'.format(proposal['value']))
        return proposal['value']

    reports = Int()
    created = Instance(datetime)
    modified = Instance(datetime)

    def to_json(self):
        ret = {}
        ret['notebook'] = self.notebook.name
        # ret['notebookid'] = self.notebook.id
        ret['interval'] = self.interval
        ret['level'] = self.level
        ret['reports'] = self.reports
        ret['created'] = self.created.strftime('%m/%d/%Y %H:%M:%S')
        ret['modified'] = self.modified.strftime('%m/%d/%Y %H:%M:%S')
        return ret

    @staticmethod
    def from_json(jsn):
        ret = JobMetadata()
        for k, v in jsn.items():
            if k in ('created', 'modified'):
                ret.set_trait(k, datetime.strptime(v, '%m/%d/%Y %H:%M:%S'))
            else:
                ret.set_trait(k, v)
        return ret


class Job(Base):
    name = Unicode()
    id = Unicode()
    meta = Instance(JobMetadata)

    def to_json(self):
        ret = {}
        ret['name'] = self.name
        ret['id'] = self.id
        ret['meta'] = self.meta.to_json()
        return ret

    def form(self):
        f = Form()
        f.entries = [
            FormEntry(name='name', type='text', label='Name', value=self.name, placeholder='Name for Job...', required=True),
            FormEntry(name='notebook', type='autocomplete', label='Notebook', url=urljoin(self.config.apiurl, 'autocomplete?type=notebooks&partial='), required=True),
            FormEntry(name='starttime', type='datetime', label='Start Time/Date', required=True),
            FormEntry(name='interval', type='select', label='Interval', options=_INTERVAL_TYPES, required=True),
            FormEntry(name='level', type='select', label='Level', options=_SERVICE_LEVELS, required=True),
            FormEntry(name='parameters_inline', type='textarea', label='Papermill params (.jsonl)', placeholder='Upload file or type here...', required=False),
            FormEntry(name='parameters', type='file', label='Papermill params (.jsonl)', required=False),
            FormEntry(name='options', type='label', label='Report options'),
            FormEntry(name='type', type='select', label='Type', options=_REPORT_TYPES, required=True),
            FormEntry(name='output', type='select', label='Output', options=_OUTPUT_TYPES, required=True),
            FormEntry(name='code', type='select', label='Strip Code', options=['yes', 'no'], required=True),
            FormEntry(name='autogen', type='checkbox', label='Autogenerate reports', value='true', required=False),
            FormEntry(name='submit', type='submit', value='Create', url=urljoin(self.config.apiurl, 'jobs'))
        ]
        return f.to_json()

    @staticmethod
    def from_json(jsn, config):
        ret = Job(config)
        ret.name = jsn['name']
        ret.id = jsn['id']
        ret.meta = JobMetadata.from_json(jsn['meta'])
        ret.meta.notebook = Notebook(config)  # FIXME
        return ret

    def edit(self):
        f = Form()
        f.entries = [
            FormEntry(name='name', type='text', value=self.name, label='Name', placeholder='Name for Job...', required=True),
            FormEntry(name='notebook', type='text', value=self.meta.notebook.name, label='Notebook', required=True, readonly=True),
            FormEntry(name='starttime', value=self.meta.start_time.strftime('%Y-%m-%dT%H:%M'), type='datetime', label='Start Time/Date', required=True),
            FormEntry(name='interval', type='select', value=self.meta.interval, label='Interval', options=_INTERVAL_TYPES, required=True),
            FormEntry(name='level', type='select', value=self.meta.level, label='Level', options=_SERVICE_LEVELS, required=True),
            FormEntry(name='reports', type='text', value=str(self.meta.reports), readonly=True),
            FormEntry(name='save', type='submit', value='save', url=urljoin(self.config.apiurl, 'jobs'))
        ]
        return f.to_json()

    def store(self):
        ret = []
        ret.append(DOMEntry(type='h2', value='Success!').to_json())
        ret.append(DOMEntry(type='p', value='Successfully configured job: {}'.format(self.name)).to_json())
        ret.append(DOMEntry(type='p', value='Notebook: {}'.format(self.meta.notebook.name)).to_json())
        return ret
