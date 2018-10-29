import json
from paperboy.scheduler._airflow import JobOperator, JobCleanupOperator, ReportOperator
from airflow import DAG
from datetime import timedelta


###################################
# Default arguments for operators #
###################################
default_args = {
    'owner': '{{owner}}',
    'start_date': '{{start_date}}'.strftime('%m/%d/%Y %H:%M:%S'),
    'email': ['{{email}}'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

###################################
# Inline job and reports as json  #
###################################
job = json.loads('{{job_json}}')
reports = json.loads('{{report_json}}')


###################################
# Create dag from job and reports #
###################################
dag = DAG('{{jobid}}', default_args=default_args)
job = JobOperator(task_id='job', dag=dag)
cleanup = JobCleanupOperator(task_id='job_cleanup', dag=dag)

for _ in range(10):
    r = ReportOperator(task_id='report_{}'.format(_), dag=dag)
    job.set_downstream(r)
    r.set_downstream(cleanup)
