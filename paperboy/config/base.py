import json
from six import string_types
from six.moves.urllib_parse import urljoin
from datetime import datetime
from traitlets import TraitType, Unicode, Int, Instance
from .forms import Form, FormElement


_INTERVAL_TYPES = ('minutely', '5 minutes', '10 minutes', '30 minutes', 'hourly', '2 hours', '3 hours', '6 hours', '12 hours', 'daily', 'weekly', 'monthly')


class NotebookMetadata(TraitType):
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


class Notebook(TraitType):
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

    def to_form(self, string=False):
        f = Form()
        f.entries = [
            FormElement(name='file', type='file', label='File', required=True),
            FormElement(name='name', type='text', label='Name', placeholder='Name for Notebook...', required=True),
            FormElement(name='privacy', type='select', label='Visibility', options=['Private', 'Public'], required=True),
            FormElement(name='sla', type='select', label='SLA', options=['Production', 'Research', 'Development', 'Personal'], required=True),
            FormElement(name='build', type='label', label='Build options'),
            FormElement(name='requirements', type='file', label='requirements.txt', required=False),
            FormElement(name='dockerfile', type='file', label='Dockerfile', required=False),
            FormElement(name='submit', type='submit', value='Create', url=urljoin(self.config.apiurl, 'notebooks')),
        ]
        if string:
            return f.to_json(string)
        return f.to_json()


class Interval(TraitType):
    default_value = 'daily'
    info_text = 'a time interval'

    def validate(self, obj, value):
        if not isinstance(value, string_types):
            self.error(obj, value)
        if value not in _INTERVAL_TYPES:
            self.error(obj, value)
        return value


class JobMetadata(TraitType):
    notebook = Notebook()
    owner = Unicode()
    interval = Interval()

    reports = Int()
    created = Instance(datetime)
    modified = Instance(datetime)

    def to_json(self, string=False):
        ret = {}
        ret['notebook'] = self.notebook
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


class Job(TraitType):
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

    def to_form(self, string=False):
        f = Form()
        f.entries = [
            FormElement(name='name', type='text', label='Name', placeholder='Name for Job...', required=True),
            FormElement(name='notebook', type='autocomplete', label='Notebook', url=urljoin(self.config.apiurl, 'autocomplete?type=notebooks&partial='), required=True),
            FormElement(name='starttime', type='datetime', label='Start Time/Date', required=True),
            FormElement(name='interval', type='select', label='Interval', options=['minutely', '5 minutes', '10 minutes', '30 minutes', 'hourly', '2 hours', '3 hours', '6 hours', '12 hours', 'daily', 'weekly', 'monthly'], required=True),
            FormElement(name='parameters_inline', type='textarea', label='Papermill params (.jsonl)', placeholder='Upload file or type here...', required=False),
            FormElement(name='parameters', type='file', label='Papermill params (.jsonl)', required=False),
            FormElement(name='options', type='label', label='Report options'),
            FormElement(name='name', type='select', label='Type', options=['Run', 'Publish'], required=True),
            FormElement(name='output', type='select', label='Output', options=['Email', 'PDF', 'HTML', 'Script'], required=True),
            FormElement(name='code', type='select', label='Strip Code', options=['Yes', 'No'], required=True),
            FormElement(name='autogen', type='checkbox', label='Autogenerate reports', value='true', required=False),
            FormElement(name='submit', type='submit', value='Create', url=urljoin(self.config.apiurl, 'jobs'))
        ]
        if string:
            return f.to_json(string)
        return f.to_json()


class ReportMetadata(TraitType):
    notebook = Notebook()
    job = Job()

    created = Instance(datetime)
    run = Instance(datetime)

    def to_json(self, string=False):
        ret = {}
        ret = {}
        ret['notebook'] = self.notebook
        ret['notebookid'] = self.notebook.id
        ret['job'] = self.job
        ret['jobid'] = self.job.id

        if self.created:
            ret['created'] = self.created.strftime('%m/%d/%Y %H:%M:%S')

        if self.run:
            ret['run'] = self.run.strftime('%m/%d/%Y %H:%M:%S')

        if string:
            return json.dumps(ret)
        return ret


class Report(TraitType):
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

    def to_form(self, string=False):
        f = Form()
        f.entries = [
            FormElement(name='name', type='text', label='Name', placeholder='Name for Report...', required=True),
            FormElement(name='notebook', type='autocomplete', label='Notebook', url=urljoin(self.config.apiurl, 'autocomplete?type=notebooks&partial='), required=True),
            FormElement(name='job', type='autocomplete', label='Job', url=urljoin(self.config.apiurl, 'autocomplete?type=jobs&partial='), required=True),
            FormElement(name='params', type='textarea', label='Parameters', placeholder='JSON Parameters...'),
            FormElement(name='type', type='select', label='Type', options=['Run', 'Publish'], required=True),
            FormElement(name='output', type='select', label='Output', options=['Email', 'PDF', 'HTML', 'Script'], required=True),
            FormElement(name='code', type='select', label='Strip Code', options=['Yes', 'No'], required=True),
            FormElement(name='submit', type='submit', value='Create', url=urljoin(self.config.apiurl, 'reports'))
        ]
        if string:
            return f.to_json(string)
        return f.to_json()
