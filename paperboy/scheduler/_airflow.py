import json
import os
import os.path
import jinja2
from datetime import datetime
from base64 import b64encode
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from paperboy.utils import name_to_class
from .base import BaseScheduler, TIMING_MAP

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'paperboy.airflow.py')), 'r') as fp:
    TEMPLATE = fp.read()


class AirflowScheduler(BaseScheduler):
    def status(self, user, params, session, *args, **kwargs):
        type = params.get('type', '')
        if type == 'notebooks':
            return []
        elif type == 'jobs':
            return []
        elif type == 'reports':
            return []
        else:
            return {'notebook': [], 'jobs': [], 'reports': []}

    def schedule(self, user, notebook, job, reports, *args, **kwargs):
        owner = user.name
        start_date = job.meta.start_time.strftime('%m/%d/%Y %H:%M:%S')
        email = 'test@test.com'
        job_json = b64encode(json.dumps(job.to_json(True)).encode('utf-8'))
        report_json = b64encode(json.dumps([r.to_json() for r in reports]).encode('utf-8'))
        interval = TIMING_MAP.get(job.meta.interval)

        tpl = jinja2.Template(TEMPLATE).render(
            owner=owner,
            start_date=start_date,
            interval=interval,
            email=email,
            job_json=job_json,
            report_json=report_json,
            output_type=self.config.output_type,
            output_dir=self.config.output_dir,
            )
        with open(os.path.join(self.config.airflow_dagbag, job.id + '.py'), 'w') as fp:
            fp.write(tpl)
        return tpl


class JobOperator(BaseOperator):
    @apply_defaults
    def __init__(self, job, *args, **kwargs):
        super(JobOperator, self).__init__(*args, **kwargs)
        self.job = job

    def execute(self, context):
        self.log.critical('job')


class JobCleanupOperator(BaseOperator):
    @apply_defaults
    def __init__(self, job, *args, **kwargs):
        super(JobCleanupOperator, self).__init__(*args, **kwargs)
        self.job = job

    def execute(self, context):
        self.log.critical('job-cleanup')


class ReportOperator(BaseOperator):
    @apply_defaults
    def __init__(self, report, *args, **kwargs):
        super(ReportOperator, self).__init__(*args, **kwargs)
        self.report = report

    def execute(self, context):
        self.log.critical('report')


class PapermillOperator(BaseOperator):
    @apply_defaults
    def __init__(self, report, *args, **kwargs):
        super(PapermillOperator, self).__init__(*args, **kwargs)
        self.report = report
        self.nbconvert_task_id = self.task_id.replace('ReportPapermill', 'ReportNBConvert')

    def execute(self, context):
        self.log.critical('papermill')

        from paperboy.worker import run_papermill
        ret = run_papermill(self.report['meta']['notebook'],
                            self.report['meta']['notebook_text'],
                            self.report['meta']['parameters'],
                            self.report['meta']['strip_code'])

        task_instance = context['task_instance']
        task_instance.xcom_push(key=self.nbconvert_task_id, value=ret)


class NBConvertOperator(BaseOperator):
    @apply_defaults
    def __init__(self, report, *args, **kwargs):
        super(NBConvertOperator, self).__init__(*args, **kwargs)
        self.report = report
        self.papermill_task_id = self.task_id.replace('ReportNBConvert', 'ReportPapermill')
        self.report_post_task_iud = self.task_id.replace('ReportNBConvert', 'ReportPost')

    def execute(self, context):
        self.log.critical('nbconvert')

        task_instance = context['task_instance']
        papermilled = task_instance.xcom_pull(task_ids=self.papermill_task_id, key=self.task_id)

        if self.report['meta']['output'] != 'notebook':
            from paperboy.worker import run_nbconvert

            template = self.report['meta'].get('template', '')

            ret = run_nbconvert(self.report['meta']['notebook'],
                                papermilled,
                                self.report['meta']['output'],
                                template,
                                self.report['meta']['strip_code'],
                                )
        else:
            ret = papermilled

        task_instance.xcom_push(key=self.report_post_task_iud, value=ret)


class ReportPostOperator(BaseOperator):
    @apply_defaults
    def __init__(self, report, config, *args, **kwargs):
        super(ReportPostOperator, self).__init__(*args, **kwargs)
        self.report = report
        self.nbconvert_task_id = self.task_id.replace('ReportPost', 'ReportNBConvert')

        self.config = name_to_class(config.get('config')).from_json(config)

    def execute(self, context):
        self.log.critical('report-post')

        task_instance = context['task_instance']
        output_nb = task_instance.xcom_pull(task_ids=self.nbconvert_task_id, key=self.task_id)
        self.log.critical(output_nb)

        outputter = self.config.clazz(self.config)
        outputter.write(self.report, output_nb, task_id=self.task_id)
