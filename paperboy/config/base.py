import json
from six.moves.urllib_parse import urljoin
from datetime import datetime
from traitlets import HasTraits, Unicode, Int, Instance, validate, TraitError
from .forms import Form, FormEntry, DOMEntry


_INTERVAL_TYPES = ('minutely', '5 minutes', '10 minutes', '30 minutes', 'hourly', '2 hours', '3 hours', '6 hours', '12 hours', 'daily', 'weekly', 'monthly')


class Base(HasTraits):
    def __init__(self, config, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        self.config = config


class User(Base):
    name = Unicode()
    id = Unicode()

    def to_json(self, string=False):
        ret = {}
        ret['name'] = self.name
        ret['id'] = self.id
        if string:
            return json.dumps(ret)
        return ret

    def form(self, string=False):
        f = Form()
        f.entries = [
            FormEntry(name='name', type='text', label='Name', placeholder='Name for Notebook...', required=True),
            FormEntry(name='submit', type='submit', value='Create', url=urljoin(self.config.apiurl, 'notebooks')),
        ]
        if string:
            return f.to_json(string)
        return f.to_json()

    @staticmethod
    def from_json(jsn, config, string=False):
        ret = User(config)
        if string:
            jsn = json.loads(jsn)
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


class NotebookMetadata(HasTraits):
    author = Unicode()
    visibility = Unicode()
    jobs = Int()
    reports = Int()
    created = Instance(datetime)
    modified = Instance(datetime)
    requirements = Unicode(allow_none=True)
    dockerfile = Unicode(allow_none=True)

    def to_json(self, string=False):
        ret = {}
        if self.author:
            ret['author'] = self.author
        if self.visibility:
            ret['visibility'] = self.visibility
        if self.jobs:
            ret['jobs'] = self.jobs
        if self.reports:
            ret['reports'] = self.reports
        if self.created:
            ret['created'] = self.created.strftime('%m/%d/%Y %H:%M:%S')
        if self.modified:
            ret['modified'] = self.modified.strftime('%m/%d/%Y %H:%M:%S')

        if string:
            return json.dumps(ret)
        return ret

    @staticmethod
    def from_json(jsn, string=False):
        ret = NotebookMetadata()
        if string:
            jsn = json.loads(jsn)
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
            FormEntry(name='file', type='file', label='File', required=True),
            FormEntry(name='name', type='text', label='Name', placeholder='Name for Notebook...', required=True),
            FormEntry(name='privacy', type='select', label='Visibility', options=['Private', 'Public'], required=True),
            FormEntry(name='sla', type='select', label='SLA', options=['Production', 'Research', 'Development', 'Personal'], required=True),
            FormEntry(name='build', type='label', label='Build options'),
            FormEntry(name='requirements', type='file', label='requirements.txt', required=False),
            FormEntry(name='dockerfile', type='file', label='Dockerfile', required=False),
            FormEntry(name='submit', type='submit', value='Create', url=urljoin(self.config.apiurl, 'notebooks')),
        ]
        if string:
            return f.to_json(string)
        return f.to_json()

    @staticmethod
    def from_json(jsn, config, string=False):
        ret = Notebook(config)
        if string:
            jsn = json.loads(jsn)
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
            FormEntry(name='privacy', type='select', label='Visibility', options=['Private', 'Public'], required=True),
            FormEntry(name='sla', type='select', label='SLA', options=['Production', 'Research', 'Development', 'Personal'], required=True),
            FormEntry(name='requirements', type='file', label='requirements.txt', required=False),
            FormEntry(name='dockerfile', type='file', label='Dockerfile', required=False),
            FormEntry(name='save', type='submit', value='save', url=urljoin(self.config.apiurl, 'notebooks'))
        ]
        return f.to_json()

    def store(self):
        ret = []
        ret.append(DOMEntry(type='p', value='Success!').to_json())
        ret.append(DOMEntry(type='p', value='Successfully stored notebook {}'.format(self.name)).to_json())
        return ret


class JobMetadata(HasTraits):
    notebook = Instance(Notebook)
    owner = Unicode()
    interval = Unicode()
    sla = Unicode()

    @validate('interval')
    def _validate_interval(self, proposal):
        if proposal['value'] not in _INTERVAL_TYPES:
            raise TraitError('Unrecognized type : {}'.format(proposal['value']))
        return proposal['value']

    reports = Int()
    created = Instance(datetime)
    modified = Instance(datetime)

    def to_json(self, string=False):
        ret = {}
        ret['notebook'] = self.notebook.name
        ret['notebookid'] = self.notebook.id

        if self.interval:
            ret['interval'] = self.interval
        if self.reports:
            ret['reports'] = self.reports
        if self.created:
            ret['created'] = self.created.strftime('%m/%d/%Y %H:%M:%S')
        if self.modified:
            ret['modified'] = self.modified.strftime('%m/%d/%Y %H:%M:%S')

        if string:
            return json.dumps(ret)
        return ret

    @staticmethod
    def from_json(jsn, string=False):
        ret = JobMetadata()
        if string:
            jsn = json.loads(jsn)
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
            FormEntry(name='name', type='text', label='Name', value=self.name, placeholder='Name for Job...', required=True),
            FormEntry(name='notebook', type='autocomplete', label='Notebook', url=urljoin(self.config.apiurl, 'autocomplete?type=notebooks&partial='), required=True),
            FormEntry(name='starttime', type='datetime', label='Start Time/Date', required=True),
            FormEntry(name='interval', type='select', label='Interval', options=['minutely', '5 minutes', '10 minutes', '30 minutes', 'hourly', '2 hours', '3 hours', '6 hours', '12 hours', 'daily', 'weekly', 'monthly'], required=True),
            FormEntry(name='sla', type='select', label='SLA', options=['Production', 'Research', 'Development', 'Personal'], required=True),
            FormEntry(name='parameters_inline', type='textarea', label='Papermill params (.jsonl)', placeholder='Upload file or type here...', required=False),
            FormEntry(name='parameters', type='file', label='Papermill params (.jsonl)', required=False),
            FormEntry(name='options', type='label', label='Report options'),
            FormEntry(name='type', type='select', label='Type', options=['Run', 'Publish'], required=True),
            FormEntry(name='output', type='select', label='Output', options=['Email', 'PDF', 'HTML', 'Script'], required=True),
            FormEntry(name='code', type='select', label='Strip Code', options=['Yes', 'No'], required=True),
            FormEntry(name='autogen', type='checkbox', label='Autogenerate reports', value='true', required=False),
            FormEntry(name='submit', type='submit', value='Create', url=urljoin(self.config.apiurl, 'jobs'))
        ]
        if string:
            return f.to_json(string)
        return f.to_json()

    @staticmethod
    def from_json(jsn, config, string=False):
        ret = Job(config)
        if string:
            jsn = json.loads(jsn)
        ret.name = jsn['name']
        ret.id = jsn['id']
        ret.meta = JobMetadata.from_json(jsn['meta'])
        ret.meta.notebook = Notebook(config)  # FIXME
        return ret

    def edit(self):
        f = Form()
        f.entries = [
            FormEntry(name='name', type='text', label='Name', value=self.name, placeholder='Name for Job...', required=True),
            FormEntry(name='starttime', type='datetime', label='Start Time/Date', required=True),
            FormEntry(name='interval', type='select', label='Interval', options=['minutely', '5 minutes', '10 minutes', '30 minutes', 'hourly', '2 hours', '3 hours', '6 hours', '12 hours', 'daily', 'weekly', 'monthly'], required=True),
            FormEntry(name='sla', type='select', label='SLA', options=['Production', 'Research', 'Development', 'Personal'], required=True),
            FormEntry(name='parameters_inline', type='textarea', label='Papermill params (.jsonl)', placeholder='Upload file or type here...', required=False),
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


class ReportMetadata(HasTraits):
    notebook = Instance(Notebook)
    job = Instance(Job)
    created = Instance(datetime)
    run = Instance(datetime)

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
