import os
import os.path
from traitlets import HasTraits, Unicode
from ..scheduler import DummyScheduler


class Scheduler(HasTraits):
    type = Unicode()


class AirflowScheduler(Scheduler):
    type = 'airflow'
    dagbag = Unicode(default_value=os.path.expanduser('~/airflow/dags'))
    clazz = DummyScheduler
