from luigi import Task
from luigi.parameter import Parameter, DateIntervalParameter, DateParameter


class BaseTask(Task):
    scheduler_interval = DateIntervalParameter()
    start_date = DateParameter()
    owner = Parameter()
    email = Parameter()


class JobTask(BaseTask):
    def __init__(self, job, *args, **kwargs):
        super(JobTask, self).__init__(*args, **kwargs)
        self.job = job

    def run(self):
        self.log.critical('job')


class JobCleanupTask(BaseTask):
    def __init__(self, job, *args, **kwargs):
        super(JobCleanupTask, self).__init__(*args, **kwargs)
        self.job = job

    def run(self):
        self.log.critical('job-cleanup')


class ReportTask(BaseTask):
    def __init__(self, report, *args, **kwargs):
        super(ReportTask, self).__init__(*args, **kwargs)
        self.report = report

    def run(self):
        self.log.critical('report')
