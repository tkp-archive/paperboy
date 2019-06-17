import luigi
from .common import BaseTask


class NBConvertTask(BaseTask):
    def __init__(self, report, *args, **kwargs):
        super(NBConvertTask, self).__init__(*args, **kwargs)
        self.report = report

    def run(self):
        self.log.critical('nbconvert')

        with open(self.input(), 'r') as fp:
            papermilled = fp.read()

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

        with open(self.output(), 'w') as fp:
            fp.write(ret)

    def output(self):
        return luigi.LocalTarget(self.report['name'])
