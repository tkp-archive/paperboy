from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from paperboy.utils import name_to_class


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
