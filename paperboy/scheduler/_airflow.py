import os
import os.path
import logging
from datetime import datetime
from airflow.models import BaseOperator
# from airflow.operators.sensors import BaseSensorOperator
from airflow.utils.decorators import apply_defaults
from .base import BaseScheduler

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'paperboy.airflow.py')), 'r') as fp:
    TEMPLATE = fp.read()


class AirflowScheduler(BaseScheduler):
    pass


class JobOperator(BaseOperator):
    @apply_defaults
    def __init__(self, job, *args, **kwargs):
        super(JobOperator, self).__init__(*args, **kwargs)
        self.job = job

    def execute(self, context):
        self.log.critical('job')
        logging.critical("job")


class JobCleanupOperator(BaseOperator):
    @apply_defaults
    def __init__(self, job, *args, **kwargs):
        super(JobCleanupOperator, self).__init__(*args, **kwargs)
        self.job = job

    def execute(self, context):
        self.log.critical('job-cleanup')
        logging.critical("job-cleanup")


class ReportOperator(BaseOperator):
    @apply_defaults
    def __init__(self, report, *args, **kwargs):
        super(ReportOperator, self).__init__(*args, **kwargs)
        self.report = report

    def execute(self, context):
        self.log.critical('report')
        logging.critical("report")


class PapermillOperator(BaseOperator):
    @apply_defaults
    def __init__(self, report, *args, **kwargs):
        super(PapermillOperator, self).__init__(*args, **kwargs)
        self.report = report
        self.nbconvert_task_id = self.task_id.replace('ReportPapermill', 'ReportNBConvert')

    def execute(self, context):
        self.log.critical('papermill')
        logging.critical("papermill")

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
        logging.critical("nbconvert")

        task_instance = context['task_instance']
        papermilled = task_instance.xcom_pull(task_ids=self.papermill_task_id, key=self.task_id)

        if self.report['meta']['output'] != 'notebook':
            from paperboy.worker import run_nbconvert

            ret = run_nbconvert(self.report['meta']['notebook'],
                                self.report['meta']['notebook_text'],
                                self.report['meta']['output'])
        else:
            ret = papermilled

        task_instance.xcom_push(key=self.report_post_task_iud, value=ret)


class ReportPostOperator(BaseOperator):
    @apply_defaults
    def __init__(self, report, output_type, *args, **kwargs):
        super(ReportPostOperator, self).__init__(*args, **kwargs)
        self.report = report
        self.output_type = output_type

        self.output_dir = kwargs.get('output_dir')
        self.nbconvert_task_id = self.task_id.replace('ReportPost', 'ReportNBConvert')

    def execute(self, context):
        self.log.critical('report-post')
        logging.critical("report-post")

        task_instance = context['task_instance']
        output_nb = task_instance.xcom_pull(task_ids=self.nbconvert_task_id, key=self.task_id)
        logging.critical(output_nb)

        path = os.path.join(self.output_dir, self.task_id) + '_' + datetime.now().strftime('%m-%d-%Y_%H-%M-%S')
        with open(path, 'wb') as fp:
            fp.write(output_nb)
