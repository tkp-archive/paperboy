import json
from base64 import b64decode
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
# Inline job and reports as b64 json  #
###################################
job = json.loads(b64decode(b'{{job_json}}'))
reports = json.loads(b64decode(b'{{report_json}}'))


###################################
# Create dag from job and reports #
###################################
dag = DAG('DAG_' + str(job['id']), default_args=default_args)
job = JobOperator(task_id=job['id'], dag=dag)
cleanup = JobCleanupOperator(task_id='job_cleanup', dag=dag)

for rep in reports:
    r = ReportOperator(task_id=rep['id'], dag=dag)
    job.set_downstream(r)
    r.set_downstream(cleanup)
