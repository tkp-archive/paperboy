import luigi
from .common import BaseTask


class PapermillTask(BaseTask):
    def __init__(self, report, *args, **kwargs):
        super(PapermillTask, self).__init__(*args, **kwargs)
        self.report = report

    def run(self, context):
        self.log.critical('papermill')

        from paperboy.worker import run_papermill
        ret = run_papermill(self.report['meta']['notebook'],
                            self.report['meta']['notebook_text'],
                            self.report['meta']['parameters'],
                            self.report['meta']['strip_code'])

        task_instance = context['task_instance']
        task_instance.xcom_push(key=self.nbconvert_task_id, value=ret)

    def output(self):
        return luigi.LocalTarget(self.report['name'])
