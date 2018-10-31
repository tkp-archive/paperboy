import json
from base64 import b64decode
from paperboy.scheduler._airflow import JobOperator, JobCleanupOperator
from paperboy.scheduler._airflow import ReportOperator, ReportPostOperator
from paperboy.scheduler._airflow import PapermillOperator, NBConvertOperator
from airflow import DAG
from datetime import timedelta, datetime


###################################
# Default arguments for operators #
###################################

# DAG args: https://airflow.incubator.apache.org/code.html?highlight=dag#airflow.models.DAG
dag_args = {
    'description': u'',
    'schedule_interval': '*/1 * * * *',
    'start_date': datetime.strptime('10/31/2018 21:15:00', '%m/%d/%Y %H:%M:%S'),
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
    'retries': 0,
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
job_json = json.loads(b64decode(b'eyJuYW1lIjogIk15Sm9iIiwgImlkIjogIkpvYi0xIiwgIm1ldGEiOiB7Im5vdGVib29rIjogIk15Tm90ZWJvb2siLCAibm90ZWJvb2tfdGV4dCI6ICJ7XG4gXCJjZWxsc1wiOiBbXG4gIHtcbiAgIFwiY2VsbF90eXBlXCI6IFwiY29kZVwiLFxuICAgXCJleGVjdXRpb25fY291bnRcIjogbnVsbCxcbiAgIFwibWV0YWRhdGFcIjoge1xuICAgIFwidGFnc1wiOiBbXG4gICAgIFwicGFyYW1ldGVyc1wiXG4gICAgXVxuICAgfSxcbiAgIFwib3V0cHV0c1wiOiBbXSxcbiAgIFwic291cmNlXCI6IFtcbiAgICBcInRpY2tlciA9ICdhYXBsJ1wiXG4gICBdXG4gIH0sXG4gIHtcbiAgIFwiY2VsbF90eXBlXCI6IFwiY29kZVwiLFxuICAgXCJleGVjdXRpb25fY291bnRcIjogbnVsbCxcbiAgIFwibWV0YWRhdGFcIjoge30sXG4gICBcIm91dHB1dHNcIjogW10sXG4gICBcInNvdXJjZVwiOiBbXG4gICAgXCJ0aWNrZXIgPSB0aWNrZXIudXBwZXIoKVxcblwiLFxuICAgIFwiXFxuXCIsXG4gICAgXCJmcm9tIElQeXRob24uZGlzcGxheSBpbXBvcnQgSFRNTFxcblwiLFxuICAgIFwiSFRNTCgnPGgxPlJlcG9ydCBmb3Ige308L2gxPicuZm9ybWF0KHRpY2tlcikpXCJcbiAgIF1cbiAgfSxcbiAge1xuICAgXCJjZWxsX3R5cGVcIjogXCJjb2RlXCIsXG4gICBcImV4ZWN1dGlvbl9jb3VudFwiOiBudWxsLFxuICAgXCJtZXRhZGF0YVwiOiB7fSxcbiAgIFwib3V0cHV0c1wiOiBbXSxcbiAgIFwic291cmNlXCI6IFtcbiAgICBcIiVtYXRwbG90bGliIGlubGluZVxcblwiLFxuICAgIFwiaW1wb3J0IHB5RVhcXG5cIixcbiAgICBcImltcG9ydCBsYW50ZXJuIGFzIGxcXG5cIixcbiAgICBcImltcG9ydCBwYW5kYXMgYXMgcGRcXG5cIixcbiAgICBcImltcG9ydCBzZWFib3JuIGFzIHNuc1xcblwiLFxuICAgIFwiXFxuXCIsXG4gICAgXCJzbnMuc2V0KClcIlxuICAgXVxuICB9LFxuICB7XG4gICBcImNlbGxfdHlwZVwiOiBcImNvZGVcIixcbiAgIFwiZXhlY3V0aW9uX2NvdW50XCI6IG51bGwsXG4gICBcIm1ldGFkYXRhXCI6IHt9LFxuICAgXCJvdXRwdXRzXCI6IFtdLFxuICAgXCJzb3VyY2VcIjogW1xuICAgIFwiSFRNTCgnPGgyPlBlcmZvcm1hbmNlPC9oMj4nKVwiXG4gICBdXG4gIH0sXG4gIHtcbiAgIFwiY2VsbF90eXBlXCI6IFwiY29kZVwiLFxuICAgXCJleGVjdXRpb25fY291bnRcIjogbnVsbCxcbiAgIFwibWV0YWRhdGFcIjoge30sXG4gICBcIm91dHB1dHNcIjogW10sXG4gICBcInNvdXJjZVwiOiBbXG4gICAgXCJkZiA9IHB5RVguY2hhcnRERih0aWNrZXIpXFxuXCIsXG4gICAgXCJsLnBsb3QoZGZbWydvcGVuJywgJ2hpZ2gnLCAnbG93JywgJ2Nsb3NlJ11dKVwiXG4gICBdXG4gIH0sXG4gIHtcbiAgIFwiY2VsbF90eXBlXCI6IFwiY29kZVwiLFxuICAgXCJleGVjdXRpb25fY291bnRcIjogbnVsbCxcbiAgIFwibWV0YWRhdGFcIjoge30sXG4gICBcIm91dHB1dHNcIjogW10sXG4gICBcInNvdXJjZVwiOiBbXG4gICAgXCJIVE1MKCc8aDI+UGVlciBDb3JyZWxhdGlvbjwvaDI+JylcIlxuICAgXVxuICB9LFxuICB7XG4gICBcImNlbGxfdHlwZVwiOiBcImNvZGVcIixcbiAgIFwiZXhlY3V0aW9uX2NvdW50XCI6IG51bGwsXG4gICBcIm1ldGFkYXRhXCI6IHt9LFxuICAgXCJvdXRwdXRzXCI6IFtdLFxuICAgXCJzb3VyY2VcIjogW1xuICAgIFwicGVlcnMgPSBweUVYLnBlZXJzKHRpY2tlcilcXG5cIixcbiAgICBcInRvX21lcmdlID0ge3g6IHB5RVguY2hhcnRERih4KSBmb3IgeCBpbiBwZWVyc31cXG5cIixcbiAgICBcInRvX21lcmdlLnVwZGF0ZSh7dGlja2VyOiBkZn0pXFxuXCIsXG4gICAgXCJhbGwgPSBzb3J0ZWQocGVlcnMgKyBbdGlja2VyXSlcXG5cIixcbiAgICBcInJldHMgPSBwZC5jb25jYXQodG9fbWVyZ2UpXFxuXCIsXG4gICAgXCJyZXRzID0gcmV0cy51bnN0YWNrKDApWydjaGFuZ2VQZXJjZW50J11bYWxsXVxcblwiLFxuICAgIFwicmV0cyA9IHJldHMuY29ycigpXFxuXCIsXG4gICAgXCJyZXRzWydzeW1ib2wnXSA9IHJldHMuaW5kZXhcXG5cIixcbiAgICBcInNucy5oZWF0bWFwKHJldHMuY29ycigpKVwiXG4gICBdXG4gIH0sXG4gIHtcbiAgIFwiY2VsbF90eXBlXCI6IFwiY29kZVwiLFxuICAgXCJleGVjdXRpb25fY291bnRcIjogbnVsbCxcbiAgIFwibWV0YWRhdGFcIjoge30sXG4gICBcIm91dHB1dHNcIjogW10sXG4gICBcInNvdXJjZVwiOiBbXVxuICB9XG4gXSxcbiBcIm1ldGFkYXRhXCI6IHtcbiAgXCJrZXJuZWxzcGVjXCI6IHtcbiAgIFwiZGlzcGxheV9uYW1lXCI6IFwiUHl0aG9uIDNcIixcbiAgIFwibGFuZ3VhZ2VcIjogXCJweXRob25cIixcbiAgIFwibmFtZVwiOiBcInB5dGhvbjNcIlxuICB9LFxuICBcImxhbmd1YWdlX2luZm9cIjoge1xuICAgXCJjb2RlbWlycm9yX21vZGVcIjoge1xuICAgIFwibmFtZVwiOiBcImlweXRob25cIixcbiAgICBcInZlcnNpb25cIjogM1xuICAgfSxcbiAgIFwiZmlsZV9leHRlbnNpb25cIjogXCIucHlcIixcbiAgIFwibWltZXR5cGVcIjogXCJ0ZXh0L3gtcHl0aG9uXCIsXG4gICBcIm5hbWVcIjogXCJweXRob25cIixcbiAgIFwibmJjb252ZXJ0X2V4cG9ydGVyXCI6IFwicHl0aG9uXCIsXG4gICBcInB5Z21lbnRzX2xleGVyXCI6IFwiaXB5dGhvbjNcIixcbiAgIFwidmVyc2lvblwiOiBcIjMuNy4wXCJcbiAgfVxuIH0sXG4gXCJuYmZvcm1hdFwiOiA0LFxuIFwibmJmb3JtYXRfbWlub3JcIjogMlxufSIsICJpbnRlcnZhbCI6ICJtaW51dGVseSIsICJsZXZlbCI6ICJwcm9kdWN0aW9uIiwgInJlcG9ydHMiOiA2LCAiY3JlYXRlZCI6ICIxMC8zMS8yMDE4IDE3OjE1OjM0IiwgIm1vZGlmaWVkIjogIjEwLzMxLzIwMTggMTc6MTU6MzQifX0='))
reports_json = json.loads(b64decode(b'W3sibmFtZSI6ICJNeUpvYi1SZXBvcnQtMCIsICJpZCI6ICJSZXBvcnQtMSIsICJtZXRhIjogeyJub3RlYm9vayI6ICJNeU5vdGVib29rIiwgImpvYiI6ICJNeUpvYiIsICJwYXJhbWV0ZXJzIjogIntcInRpY2tlclwiOiBcIkFBUExcIn0iLCAidHlwZSI6ICJydW4iLCAib3V0cHV0IjogInBkZiIsICJzdHJpcF9jb2RlIjogZmFsc2UsICJydW4iOiAibm90IHJ1biIsICJjcmVhdGVkIjogIjEwLzMxLzIwMTggMTc6MTU6MzQiLCAibW9kaWZpZWQiOiAiMTAvMzEvMjAxOCAxNzoxNTozNCJ9fSwgeyJuYW1lIjogIk15Sm9iLVJlcG9ydC0xIiwgImlkIjogIlJlcG9ydC0yIiwgIm1ldGEiOiB7Im5vdGVib29rIjogIk15Tm90ZWJvb2siLCAiam9iIjogIk15Sm9iIiwgInBhcmFtZXRlcnMiOiAie1widGlja2VyXCI6IFwiRkJcIn0iLCAidHlwZSI6ICJydW4iLCAib3V0cHV0IjogInBkZiIsICJzdHJpcF9jb2RlIjogZmFsc2UsICJydW4iOiAibm90IHJ1biIsICJjcmVhdGVkIjogIjEwLzMxLzIwMTggMTc6MTU6MzQiLCAibW9kaWZpZWQiOiAiMTAvMzEvMjAxOCAxNzoxNTozNCJ9fSwgeyJuYW1lIjogIk15Sm9iLVJlcG9ydC0yIiwgImlkIjogIlJlcG9ydC0zIiwgIm1ldGEiOiB7Im5vdGVib29rIjogIk15Tm90ZWJvb2siLCAiam9iIjogIk15Sm9iIiwgInBhcmFtZXRlcnMiOiAie1widGlja2VyXCI6IFwiR09PR0xcIn0iLCAidHlwZSI6ICJydW4iLCAib3V0cHV0IjogInBkZiIsICJzdHJpcF9jb2RlIjogZmFsc2UsICJydW4iOiAibm90IHJ1biIsICJjcmVhdGVkIjogIjEwLzMxLzIwMTggMTc6MTU6MzQiLCAibW9kaWZpZWQiOiAiMTAvMzEvMjAxOCAxNzoxNTozNCJ9fSwgeyJuYW1lIjogIk15Sm9iLVJlcG9ydC0zIiwgImlkIjogIlJlcG9ydC00IiwgIm1ldGEiOiB7Im5vdGVib29rIjogIk15Tm90ZWJvb2siLCAiam9iIjogIk15Sm9iIiwgInBhcmFtZXRlcnMiOiAie1widGlja2VyXCI6IFwiSUJNXCJ9IiwgInR5cGUiOiAicnVuIiwgIm91dHB1dCI6ICJwZGYiLCAic3RyaXBfY29kZSI6IGZhbHNlLCAicnVuIjogIm5vdCBydW4iLCAiY3JlYXRlZCI6ICIxMC8zMS8yMDE4IDE3OjE1OjM0IiwgIm1vZGlmaWVkIjogIjEwLzMxLzIwMTggMTc6MTU6MzQifX0sIHsibmFtZSI6ICJNeUpvYi1SZXBvcnQtNCIsICJpZCI6ICJSZXBvcnQtNSIsICJtZXRhIjogeyJub3RlYm9vayI6ICJNeU5vdGVib29rIiwgImpvYiI6ICJNeUpvYiIsICJwYXJhbWV0ZXJzIjogIntcInRpY2tlclwiOiBcIk1TRlRcIn0iLCAidHlwZSI6ICJydW4iLCAib3V0cHV0IjogInBkZiIsICJzdHJpcF9jb2RlIjogZmFsc2UsICJydW4iOiAibm90IHJ1biIsICJjcmVhdGVkIjogIjEwLzMxLzIwMTggMTc6MTU6MzQiLCAibW9kaWZpZWQiOiAiMTAvMzEvMjAxOCAxNzoxNTozNCJ9fSwgeyJuYW1lIjogIk15Sm9iLVJlcG9ydC01IiwgImlkIjogIlJlcG9ydC02IiwgIm1ldGEiOiB7Im5vdGVib29rIjogIk15Tm90ZWJvb2siLCAiam9iIjogIk15Sm9iIiwgInBhcmFtZXRlcnMiOiAie1widGlja2VyXCI6IFwiTkZMWFwifSIsICJ0eXBlIjogInJ1biIsICJvdXRwdXQiOiAicGRmIiwgInN0cmlwX2NvZGUiOiBmYWxzZSwgInJ1biI6ICJub3QgcnVuIiwgImNyZWF0ZWQiOiAiMTAvMzEvMjAxOCAxNzoxNTozNCIsICJtb2RpZmllZCI6ICIxMC8zMS8yMDE4IDE3OjE1OjM0In19XQ=='))


###################################
# Create dag from job and reports #
###################################

# The top level dag, representing a Job run on a Notebook
dag = DAG('DAG-' + str(job_json['id']), default_args=default_operator_args, **dag_args)

# The Job operator, used for bundling groups of reports,
# setting up env/image
job = JobOperator(job=job_json, task_id='Job-{}'.format(job_json['id']), dag=dag)

# The cleanup operator, run after all reports are finished
cleanup = JobCleanupOperator(job=job_json, task_id='JobCleanup-{}'.format(job_json['id']), dag=dag)

for rep in reports_json:
    # copy over notebook text (only store 1 copy in the job json)
    rep['meta']['notebook_text'] = job_json['meta']['notebook_text']

    # Report operator, performs the required
    # steps prior to running the report
    r = ReportOperator(report=rep, task_id='Report-{}'.format(rep['id']), dag=dag)

    # Papermill operator, performs the report creation
    # using papermill and the report's individual
    # parameters and configuration
    pp = PapermillOperator(report=rep, task_id='ReportPapermill-{}'.format(rep['id']), dag=dag)

    # NBConvert operator, performs the NBConversion if
    # required
    nb = NBConvertOperator(report=rep, task_id='ReportNBConvert-{}'.format(rep['id']), dag=dag)

    # The post-report operator, used for post-report
    # tasks such as sending the report in an email,
    # deploying the report to a webserver, etc
    rp = ReportPostOperator(report=rep,
                            output_type='directory',
                            output_dir='/Users/theocean154/Downloads',
                            task_id='ReportPost-{}'.format(rep['id']), dag=dag)

    # Job -> Report -> ReportPost -\
    #   \--> Report -> ReportPost --\
    #    \-> Report -> ReportPost ----> Job Cleanup
    job.set_downstream(r)
    r.set_downstream(pp)
    pp.set_downstream(nb)
    nb.set_downstream(rp)
    rp.set_downstream(cleanup)
