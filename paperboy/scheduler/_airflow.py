import os
import os.path
import logging
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


class ReportPostOperator(BaseOperator):
    @apply_defaults
    def __init__(self, report, *args, **kwargs):
        super(ReportPostOperator, self).__init__(*args, **kwargs)
        self.report = report

    def execute(self, context):
        self.log.critical('report-post')
        logging.critical("report-post")
