import os
import os.path
from traitlets import HasTraits, Unicode
from ..scheduler import DummyScheduler


class SchedulerConfig(HasTraits):
    type = Unicode()


class AirflowSchedulerConfig(SchedulerConfig):
    type = 'airflow'
    dagbag = Unicode(default_value=os.path.expanduser('~/airflow/dags'))
    config = Unicode(default_value=os.path.expanduser('~/airflow/airflow.cfg'))
    clazz = DummyScheduler
