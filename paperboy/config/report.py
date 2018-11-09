import os
import os.path
from six.moves.urllib_parse import urljoin
from datetime import datetime
from traitlets import HasTraits, Unicode, Instance, Bool
from .forms import Response, FormEntry, DOMEntry
from .base import Base, _REPORT_TYPES, _OUTPUT_TYPES
from .notebook import NotebookConfig
from .job import JobConfig


TEMPLATE_BASEPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'worker', 'nbconvert_templates'))


def _type_to_template(output, strip_code):
    if output in ('pdf', 'html'):
        ret = output
        if output == 'pdf':
            ret += '.tplx'
        else:
            ret += '.tpl'
        return ret
    elif output == 'email':
        ret = 'html_email'
        ret += '.tpl'
        return ret
    else:
        return ''


class ReportMetadataConfig(HasTraits):
    notebook = Instance(NotebookConfig)
    job = Instance(JobConfig)

    username = Unicode()
    userid = Unicode()

    run = Instance(datetime)
    parameters = Unicode()
    type = Unicode()
    output = Unicode()
    strip_code = Bool()

    template = Unicode()

    run = Instance(datetime, allow_none=True)
    created = Instance(datetime)
    modified = Instance(datetime)

    def to_json(self, include_notebook=False):
        ret = {}
        ret = {}
        ret['notebook'] = self.notebook.name
        if include_notebook:
            ret['notebook_text'] = self.notebook.meta.notebook
        # ret['notebookid'] = self.notebook.id

        ret['job'] = self.job.name
        # ret['jobid'] = self.job.id

        ret['parameters'] = self.parameters
        ret['type'] = self.type
        ret['output'] = self.output
        ret['strip_code'] = self.strip_code

        ret['template'] = self.template or os.path.join(TEMPLATE_BASEPATH, _type_to_template(self.output, self.strip_code))

        if self.run:
            ret['run'] = self.run.strftime('%m/%d/%Y %H:%M:%S')
        else:
            ret['run'] = 'not run'
        ret['created'] = self.created.strftime('%m/%d/%Y %H:%M:%S')
        ret['modified'] = self.modified.strftime('%m/%d/%Y %H:%M:%S')

        return ret

    @staticmethod
    def from_json(jsn):
        ret = ReportMetadataConfig()
        for k, v in jsn.items():
            if k in ('created', 'modified', 'run'):
                ret.set_trait(k, datetime.strptime(v, '%m/%d/%Y %H:%M:%S'))
            else:
                ret.set_trait(k, v)
        return ret


class ReportConfig(Base):
    name = Unicode()
    id = Unicode()
    meta = Instance(ReportMetadataConfig)

    def to_json(self, include_notebook=False):
        ret = {}
        ret['name'] = self.name
        ret['id'] = self.id
        ret['meta'] = self.meta.to_json(include_notebook)
        return ret

    def form(self):
        f = Response()
        f.entries = [
            FormEntry(name='name', type='text', label='Name', placeholder='Name for Report...', required=True),
            FormEntry(name='notebook', type='autocomplete', label='Notebook', url=urljoin(self.config.apiurl, 'autocomplete?type=notebooks&partial='), required=True),
            FormEntry(name='job', type='autocomplete', label='Job', url=urljoin(self.config.apiurl, 'autocomplete?type=jobs&partial='), required=True),
            FormEntry(name='parameters', type='textarea', label='Parameters', placeholder='JSON Parameters...'),
            FormEntry(name='type', type='select', label='Type', options=_REPORT_TYPES, required=True),
            FormEntry(name='output', type='select', label='Output', options=_OUTPUT_TYPES, required=True),
            FormEntry(name='code', type='select', label='Strip Code', options=['yes', 'no'], required=True),
            FormEntry(name='template', type='text', label='Template', required=False),
            FormEntry(name='submit', type='submit', value='Create', url=urljoin(self.config.apiurl, 'reports'))
        ]
        return f.to_json()

    @staticmethod
    def from_json(jsn, config):
        ret = ReportConfig(config)
        ret.name = jsn['name']
        ret.id = jsn['id']
        ret.meta = ReportMetadataConfig.from_json(jsn['meta'])
        ret.meta.notebook = NotebookConfig(config)
        ret.meta.job = JobConfig(config)
        return ret

    def edit(self):
        f = Response()
        f.entries = [
            FormEntry(name='name', type='text', value=self.name, label='Name', placeholder='Name for Report...', required=True),
            FormEntry(name='notebook', type='text', value=self.meta.notebook.name, label='Notebook', required=True, readonly=True),
            FormEntry(name='job', type='text', value=self.meta.job.name, label='Job', required=True, readonly=True),
            FormEntry(name='parameters', type='textarea', value=self.meta.parameters, label='Parameters', placeholder='JSON Parameters...'),
            FormEntry(name='type', type='select', value=self.meta.type, label='Type', options=_REPORT_TYPES, required=True),
            FormEntry(name='output', type='select', value=self.meta.output, label='Output', options=_OUTPUT_TYPES, required=True),
            FormEntry(name='code', type='select', value='yes' if self.meta.strip_code else 'no', label='Strip Code', options=['yes', 'no'], required=True),
            FormEntry(name='save', type='submit', value='save', url=urljoin(self.config.apiurl, 'jobs'))
        ]
        return f.to_json()

    def store(self):
        ret = Response()
        ret.entries = [
            DOMEntry(type='h2', value='Success!'),
            DOMEntry(type='p', value='Successfully configured report: {}!'.format(self.name)),
            DOMEntry(type='p', value='Notebook: {}'.format(self.meta.notebook.name)),
            DOMEntry(type='p', value='Job: {}'.format(self.meta.job.name)),
        ]
        return ret.to_json()

    def row(self):
        f = Response()
        f.entries = [
            DOMEntry(name='name', type='text', value=self.name, label='Name', placeholder='Name for Report...', required=True),
            DOMEntry(name='notebook', type='jsondl', value=self.meta.notebook.name, label='Notebook', required=True, readonly=True),
            DOMEntry(name='job', type='text', value=self.meta.job.name, label='Job', required=True, readonly=True),
            DOMEntry(name='parameters', type='textarea', value=self.meta.parameters, label='Parameters', placeholder='JSON Parameters...'),
            DOMEntry(name='type', type='select', value=self.meta.type, label='Type', options=_REPORT_TYPES, required=True),
            DOMEntry(name='output', type='select', value=self.meta.output, label='Output', options=_OUTPUT_TYPES, required=True),
            DOMEntry(name='code', type='select', value='yes' if self.meta.strip_code else 'no', label='Strip Code', options=['yes', 'no'], required=True),
        ]
        return f.to_json()
