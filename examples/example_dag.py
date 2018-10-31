import json
from base64 import b64decode
from paperboy.scheduler._airflow import JobOperator, JobCleanupOperator, ReportOperator, ReportPostOperator
from airflow import DAG
from datetime import timedelta, datetime


###################################
# Default arguments for operators #
###################################

# DAG args: https://airflow.incubator.apache.org/code.html?highlight=dag#airflow.models.DAG
dag_args = {
    'description': u'',
    'schedule_interval': '*/1 * * * *',
    'start_date': datetime.strptime('10/31/2018 01:50:00', '%m/%d/%Y %H:%M:%S'),
    'end_date': None,
    'full_filepath': None,
    'template_searchpath': None,
    'user_defined_macros': None,
    'user_defined_filters': None,
    'concurrency': 16,
    'max_active_runs': 16,
    'dagrun_timeout': None,
    'sla_miss_callback': None,
    'default_view': u'graph',
    'orientation': 'LR',
    'catchup': False,
    'on_success_callback': None,
    'on_failure_callback': None,
    # 'params': None,
}

# Operator args: https://airflow.incubator.apache.org/code.html#baseoperator
default_operator_args = {
    'owner': 'test',
    'email': ['test@test.com'],
    'email_on_retry': False,
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'retry_exponential_backoff': False,
    'max_retry_delay': None,
    'start_date': None,
    'end_date': None,
    'schedule_interval': None,
    'depends_on_past': False,
    'wait_for_downstream': False,
    # 'params': None,
    'default_args': None,
    'adhoc': False,
    'priority_weight': 1,
    'weight_rule': u'downstream',
    'queue': 'default',
    'pool': None,
    'sla': None,
    'execution_timeout': None,
    'on_failure_callback': None,
    'on_success_callback': None,
    'on_retry_callback': None,
    'trigger_rule': u'all_success',
    'resources': None,
    'run_as_user': None,
    'task_concurrency': None,
    'executor_config': None,
    'inlets': None,
    'outlets': None,
}

###################################
# Inline job and reports as b64 json  #
###################################
job_json = json.loads(b64decode(b'eyJuYW1lIjogIk15Sm9iIiwgImlkIjogIkpvYi0xIiwgIm1ldGEiOiB7Im5vdGVib29rIjogIk15Tm90ZWJvb2siLCAiaW50ZXJ2YWwiOiAibWludXRlbHkiLCAibGV2ZWwiOiAicHJvZHVjdGlvbiIsICJyZXBvcnRzIjogNiwgImNyZWF0ZWQiOiAiMTAvMzAvMjAxOCAyMTo1MDo1MiIsICJtb2RpZmllZCI6ICIxMC8zMC8yMDE4IDIxOjUwOjUyIn19'))
reports_json = json.loads(b64decode(b'W3sibmFtZSI6ICJNeUpvYi1SZXBvcnQtMCIsICJpZCI6ICJSZXBvcnQtMSIsICJtZXRhIjogeyJub3RlYm9vayI6ICJNeU5vdGVib29rIiwgImpvYiI6ICJNeUpvYiIsICJwYXJhbWV0ZXJzIjogIntcInRpY2tlclwiOiBcIkFBUExcIn0iLCAidHlwZSI6ICJydW4iLCAib3V0cHV0IjogIm5vdGVib29rIiwgInN0cmlwX2NvZGUiOiB0cnVlLCAicnVuIjogIm5vdCBydW4iLCAiY3JlYXRlZCI6ICIxMC8zMC8yMDE4IDIxOjUwOjUyIiwgIm1vZGlmaWVkIjogIjEwLzMwLzIwMTggMjE6NTA6NTIifX0sIHsibmFtZSI6ICJNeUpvYi1SZXBvcnQtMSIsICJpZCI6ICJSZXBvcnQtMiIsICJtZXRhIjogeyJub3RlYm9vayI6ICJNeU5vdGVib29rIiwgImpvYiI6ICJNeUpvYiIsICJwYXJhbWV0ZXJzIjogIntcInRpY2tlclwiOiBcIkZCXCJ9IiwgInR5cGUiOiAicnVuIiwgIm91dHB1dCI6ICJub3RlYm9vayIsICJzdHJpcF9jb2RlIjogdHJ1ZSwgInJ1biI6ICJub3QgcnVuIiwgImNyZWF0ZWQiOiAiMTAvMzAvMjAxOCAyMTo1MDo1MiIsICJtb2RpZmllZCI6ICIxMC8zMC8yMDE4IDIxOjUwOjUyIn19LCB7Im5hbWUiOiAiTXlKb2ItUmVwb3J0LTIiLCAiaWQiOiAiUmVwb3J0LTMiLCAibWV0YSI6IHsibm90ZWJvb2siOiAiTXlOb3RlYm9vayIsICJqb2IiOiAiTXlKb2IiLCAicGFyYW1ldGVycyI6ICJ7XCJ0aWNrZXJcIjogXCJHT09HTFwifSIsICJ0eXBlIjogInJ1biIsICJvdXRwdXQiOiAibm90ZWJvb2siLCAic3RyaXBfY29kZSI6IHRydWUsICJydW4iOiAibm90IHJ1biIsICJjcmVhdGVkIjogIjEwLzMwLzIwMTggMjE6NTA6NTIiLCAibW9kaWZpZWQiOiAiMTAvMzAvMjAxOCAyMTo1MDo1MiJ9fSwgeyJuYW1lIjogIk15Sm9iLVJlcG9ydC0zIiwgImlkIjogIlJlcG9ydC00IiwgIm1ldGEiOiB7Im5vdGVib29rIjogIk15Tm90ZWJvb2siLCAiam9iIjogIk15Sm9iIiwgInBhcmFtZXRlcnMiOiAie1widGlja2VyXCI6IFwiSUJNXCJ9IiwgInR5cGUiOiAicnVuIiwgIm91dHB1dCI6ICJub3RlYm9vayIsICJzdHJpcF9jb2RlIjogdHJ1ZSwgInJ1biI6ICJub3QgcnVuIiwgImNyZWF0ZWQiOiAiMTAvMzAvMjAxOCAyMTo1MDo1MiIsICJtb2RpZmllZCI6ICIxMC8zMC8yMDE4IDIxOjUwOjUyIn19LCB7Im5hbWUiOiAiTXlKb2ItUmVwb3J0LTQiLCAiaWQiOiAiUmVwb3J0LTUiLCAibWV0YSI6IHsibm90ZWJvb2siOiAiTXlOb3RlYm9vayIsICJqb2IiOiAiTXlKb2IiLCAicGFyYW1ldGVycyI6ICJ7XCJ0aWNrZXJcIjogXCJNU0ZUXCJ9IiwgInR5cGUiOiAicnVuIiwgIm91dHB1dCI6ICJub3RlYm9vayIsICJzdHJpcF9jb2RlIjogdHJ1ZSwgInJ1biI6ICJub3QgcnVuIiwgImNyZWF0ZWQiOiAiMTAvMzAvMjAxOCAyMTo1MDo1MiIsICJtb2RpZmllZCI6ICIxMC8zMC8yMDE4IDIxOjUwOjUyIn19LCB7Im5hbWUiOiAiTXlKb2ItUmVwb3J0LTUiLCAiaWQiOiAiUmVwb3J0LTYiLCAibWV0YSI6IHsibm90ZWJvb2siOiAiTXlOb3RlYm9vayIsICJqb2IiOiAiTXlKb2IiLCAicGFyYW1ldGVycyI6ICJ7XCJ0aWNrZXJcIjogXCJORkxYXCJ9IiwgInR5cGUiOiAicnVuIiwgIm91dHB1dCI6ICJub3RlYm9vayIsICJzdHJpcF9jb2RlIjogdHJ1ZSwgInJ1biI6ICJub3QgcnVuIiwgImNyZWF0ZWQiOiAiMTAvMzAvMjAxOCAyMTo1MDo1MiIsICJtb2RpZmllZCI6ICIxMC8zMC8yMDE4IDIxOjUwOjUyIn19XQ=='))


###################################
# Create dag from job and reports #
###################################

# The top level dag, representing a Job run on a Notebook
dag = DAG('DAG_' + str(job_json['id']), default_args=default_operator_args, **dag_args)

# The Job operator, used for bundling groups of reports,
# setting up env/image
job = JobOperator(job=job_json, task_id='Job-{}'.format(job_json['id']), dag=dag)

# The cleanup operator, run after all reports are finished
cleanup = JobCleanupOperator(job=job_json, task_id='JobCleanup-{}'.format(job_json['id']), dag=dag)

for rep in reports_json:
    # Report operator, performs the report creation
    # using papermill and the report's individual
    # parameters and configuration
    r = ReportOperator(report=rep, task_id='Report-{}'.format(rep['id']), dag=dag)

    # The post-report operator, used for post-report
    # tasks such as sending the report in an email,
    # deploying the report to a webserver, etc
    rp = ReportPostOperator(report=rep, task_id='ReportPost-{}'.format(rep['id']), dag=dag)

    # Job -> Report -> ReportPost -\
    #   \--> Report -> ReportPost --\
    #    \-> Report -> ReportPost ----> Job Cleanup
    job.set_downstream(r)
    r.set_downstream(rp)
    rp.set_downstream(cleanup)
