import logging
from airflow.models import BaseOperator
# from airflow.operators.sensors import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

from .base import BaseScheduler


class AirflowScheduler(BaseScheduler):
    pass


class JobOperator(BaseOperator):
    @apply_defaults
    def __init__(self, reports, after=None, *args, **kwargs):
        super(JobOperator, self).__init__(*args, **kwargs)
        for report in reports:
            self.set_downstream(report)
            if after:
                report.set_downstream(after)

    def execute(self, context):
        logging.info("job")


class JobCleanupOperator(BaseOperator):
    @apply_defaults
    def __init__(self, *args, **kwargs):
        super(JobCleanupOperator, self).__init__(*args, **kwargs)

    def execute(self, context):
        logging.info("job-cleanup")


class ReportOperator(BaseOperator):
    @apply_defaults
    def __init__(self, *args, **kwargs):
        super(ReportOperator, self).__init__(*args, **kwargs)

    def execute(self, context):
        logging.info("report")


# class Sensor(BaseSensorOperator):
#     @apply_defaults
#     def __init__(self, *args, **kwargs):
#         super(Sensor, self).__init__(*args, **kwargs)

#     def poke(self, context):
#         current_minute = datetime.now().minute
#         if current_minute % 3 != 0:
#             logging.info("Current minute (%s) not is divisible by 3, sensor will retry.", current_minute)
#             return False

#         logging.info("Current minute (%s) is divisible by 3, sensor finishing.", current_minute)
#         return True
