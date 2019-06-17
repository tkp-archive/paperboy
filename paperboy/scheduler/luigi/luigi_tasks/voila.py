from .common import BaseTask
from paperboy.utils import name_to_class


class VoilaTask(BaseTask):
    def __init__(self, report, config, *args, **kwargs):
        super(VoilaTask, self).__init__(*args, **kwargs)
        self.report = report
        self.config = name_to_class(config.get('config')).from_json(config)

    def run(self, context):
        self.log.critical('report-post')

        with open(self.input(), 'r') as fp:
            output_nb = fp.read()
        self.log.critical(output_nb)

        outputter = self.config.clazz(self.config)
        outputter.write(self.report, output_nb, task_id=self.task_id)
