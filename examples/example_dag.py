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
    'start_date': datetime.strptime('10/31/2018 20:43:00', '%m/%d/%Y %H:%M:%S'),
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
job_json = json.loads(b64decode(b'eyJuYW1lIjogIk15Sm9iMiIsICJpZCI6ICJKb2ItMiIsICJtZXRhIjogeyJub3RlYm9vayI6ICJNeU5vdGVib29rIiwgIm5vdGVib29rX3RleHQiOiAie1xuIFwiY2VsbHNcIjogW1xuICB7XG4gICBcImNlbGxfdHlwZVwiOiBcImNvZGVcIixcbiAgIFwiZXhlY3V0aW9uX2NvdW50XCI6IG51bGwsXG4gICBcIm1ldGFkYXRhXCI6IHtcbiAgICBcInRhZ3NcIjogW1xuICAgICBcInBhcmFtZXRlcnNcIlxuICAgIF1cbiAgIH0sXG4gICBcIm91dHB1dHNcIjogW10sXG4gICBcInNvdXJjZVwiOiBbXG4gICAgXCJ0aWNrZXIgPSAnYWFwbCdcIlxuICAgXVxuICB9LFxuICB7XG4gICBcImNlbGxfdHlwZVwiOiBcImNvZGVcIixcbiAgIFwiZXhlY3V0aW9uX2NvdW50XCI6IG51bGwsXG4gICBcIm1ldGFkYXRhXCI6IHt9LFxuICAgXCJvdXRwdXRzXCI6IFtdLFxuICAgXCJzb3VyY2VcIjogW1xuICAgIFwidGlja2VyID0gdGlja2VyLnVwcGVyKClcXG5cIixcbiAgICBcIlxcblwiLFxuICAgIFwiZnJvbSBJUHl0aG9uLmRpc3BsYXkgaW1wb3J0IEhUTUxcXG5cIixcbiAgICBcIkhUTUwoJzxoMT5SZXBvcnQgZm9yIHt9PC9oMT4nLmZvcm1hdCh0aWNrZXIpKVwiXG4gICBdXG4gIH0sXG4gIHtcbiAgIFwiY2VsbF90eXBlXCI6IFwiY29kZVwiLFxuICAgXCJleGVjdXRpb25fY291bnRcIjogbnVsbCxcbiAgIFwibWV0YWRhdGFcIjoge30sXG4gICBcIm91dHB1dHNcIjogW10sXG4gICBcInNvdXJjZVwiOiBbXG4gICAgXCIlbWF0cGxvdGxpYiBpbmxpbmVcXG5cIixcbiAgICBcImltcG9ydCBweUVYXFxuXCIsXG4gICAgXCJpbXBvcnQgbGFudGVybiBhcyBsXFxuXCIsXG4gICAgXCJpbXBvcnQgcGFuZGFzIGFzIHBkXFxuXCIsXG4gICAgXCJpbXBvcnQgc2VhYm9ybiBhcyBzbnNcXG5cIixcbiAgICBcIlxcblwiLFxuICAgIFwic25zLnNldCgpXCJcbiAgIF1cbiAgfSxcbiAge1xuICAgXCJjZWxsX3R5cGVcIjogXCJjb2RlXCIsXG4gICBcImV4ZWN1dGlvbl9jb3VudFwiOiBudWxsLFxuICAgXCJtZXRhZGF0YVwiOiB7fSxcbiAgIFwib3V0cHV0c1wiOiBbXSxcbiAgIFwic291cmNlXCI6IFtcbiAgICBcIkhUTUwoJzxoMj5QZXJmb3JtYW5jZTwvaDI+JylcIlxuICAgXVxuICB9LFxuICB7XG4gICBcImNlbGxfdHlwZVwiOiBcImNvZGVcIixcbiAgIFwiZXhlY3V0aW9uX2NvdW50XCI6IG51bGwsXG4gICBcIm1ldGFkYXRhXCI6IHt9LFxuICAgXCJvdXRwdXRzXCI6IFtdLFxuICAgXCJzb3VyY2VcIjogW1xuICAgIFwiZGYgPSBweUVYLmNoYXJ0REYodGlja2VyKVxcblwiLFxuICAgIFwibC5wbG90KGRmW1snb3BlbicsICdoaWdoJywgJ2xvdycsICdjbG9zZSddXSlcIlxuICAgXVxuICB9LFxuICB7XG4gICBcImNlbGxfdHlwZVwiOiBcImNvZGVcIixcbiAgIFwiZXhlY3V0aW9uX2NvdW50XCI6IG51bGwsXG4gICBcIm1ldGFkYXRhXCI6IHt9LFxuICAgXCJvdXRwdXRzXCI6IFtdLFxuICAgXCJzb3VyY2VcIjogW1xuICAgIFwiSFRNTCgnPGgyPlBlZXIgQ29ycmVsYXRpb248L2gyPicpXCJcbiAgIF1cbiAgfSxcbiAge1xuICAgXCJjZWxsX3R5cGVcIjogXCJjb2RlXCIsXG4gICBcImV4ZWN1dGlvbl9jb3VudFwiOiBudWxsLFxuICAgXCJtZXRhZGF0YVwiOiB7fSxcbiAgIFwib3V0cHV0c1wiOiBbXSxcbiAgIFwic291cmNlXCI6IFtcbiAgICBcInBlZXJzID0gcHlFWC5wZWVycyh0aWNrZXIpXFxuXCIsXG4gICAgXCJ0b19tZXJnZSA9IHt4OiBweUVYLmNoYXJ0REYoeCkgZm9yIHggaW4gcGVlcnN9XFxuXCIsXG4gICAgXCJ0b19tZXJnZS51cGRhdGUoe3RpY2tlcjogZGZ9KVxcblwiLFxuICAgIFwiYWxsID0gc29ydGVkKHBlZXJzICsgW3RpY2tlcl0pXFxuXCIsXG4gICAgXCJyZXRzID0gcGQuY29uY2F0KHRvX21lcmdlKVxcblwiLFxuICAgIFwicmV0cyA9IHJldHMudW5zdGFjaygwKVsnY2hhbmdlUGVyY2VudCddW2FsbF1cXG5cIixcbiAgICBcInJldHMgPSByZXRzLmNvcnIoKVxcblwiLFxuICAgIFwicmV0c1snc3ltYm9sJ10gPSByZXRzLmluZGV4XFxuXCIsXG4gICAgXCJzbnMuaGVhdG1hcChyZXRzLmNvcnIoKSlcIlxuICAgXVxuICB9LFxuICB7XG4gICBcImNlbGxfdHlwZVwiOiBcImNvZGVcIixcbiAgIFwiZXhlY3V0aW9uX2NvdW50XCI6IG51bGwsXG4gICBcIm1ldGFkYXRhXCI6IHt9LFxuICAgXCJvdXRwdXRzXCI6IFtdLFxuICAgXCJzb3VyY2VcIjogW11cbiAgfVxuIF0sXG4gXCJtZXRhZGF0YVwiOiB7XG4gIFwia2VybmVsc3BlY1wiOiB7XG4gICBcImRpc3BsYXlfbmFtZVwiOiBcIlB5dGhvbiAzXCIsXG4gICBcImxhbmd1YWdlXCI6IFwicHl0aG9uXCIsXG4gICBcIm5hbWVcIjogXCJweXRob24zXCJcbiAgfSxcbiAgXCJsYW5ndWFnZV9pbmZvXCI6IHtcbiAgIFwiY29kZW1pcnJvcl9tb2RlXCI6IHtcbiAgICBcIm5hbWVcIjogXCJpcHl0aG9uXCIsXG4gICAgXCJ2ZXJzaW9uXCI6IDNcbiAgIH0sXG4gICBcImZpbGVfZXh0ZW5zaW9uXCI6IFwiLnB5XCIsXG4gICBcIm1pbWV0eXBlXCI6IFwidGV4dC94LXB5dGhvblwiLFxuICAgXCJuYW1lXCI6IFwicHl0aG9uXCIsXG4gICBcIm5iY29udmVydF9leHBvcnRlclwiOiBcInB5dGhvblwiLFxuICAgXCJweWdtZW50c19sZXhlclwiOiBcImlweXRob24zXCIsXG4gICBcInZlcnNpb25cIjogXCIzLjcuMFwiXG4gIH1cbiB9LFxuIFwibmJmb3JtYXRcIjogNCxcbiBcIm5iZm9ybWF0X21pbm9yXCI6IDJcbn0iLCAiaW50ZXJ2YWwiOiAibWludXRlbHkiLCAibGV2ZWwiOiAicHJvZHVjdGlvbiIsICJyZXBvcnRzIjogNiwgImNyZWF0ZWQiOiAiMTAvMzEvMjAxOCAxNjo0Mzo0NyIsICJtb2RpZmllZCI6ICIxMC8zMS8yMDE4IDE2OjQzOjQ3In19'))
reports_json = json.loads(b64decode(b'W3sibmFtZSI6ICJNeUpvYjItUmVwb3J0LTAiLCAiaWQiOiAiUmVwb3J0LTciLCAibWV0YSI6IHsibm90ZWJvb2siOiAiTXlOb3RlYm9vayIsICJqb2IiOiAiTXlKb2IyIiwgInBhcmFtZXRlcnMiOiAie1widGlja2VyXCI6IFwiQUFQTFwifSIsICJ0eXBlIjogInJ1biIsICJvdXRwdXQiOiAicGRmIiwgInN0cmlwX2NvZGUiOiB0cnVlLCAicnVuIjogIm5vdCBydW4iLCAiY3JlYXRlZCI6ICIxMC8zMS8yMDE4IDE2OjQzOjQ3IiwgIm1vZGlmaWVkIjogIjEwLzMxLzIwMTggMTY6NDM6NDcifX0sIHsibmFtZSI6ICJNeUpvYjItUmVwb3J0LTEiLCAiaWQiOiAiUmVwb3J0LTgiLCAibWV0YSI6IHsibm90ZWJvb2siOiAiTXlOb3RlYm9vayIsICJqb2IiOiAiTXlKb2IyIiwgInBhcmFtZXRlcnMiOiAie1widGlja2VyXCI6IFwiRkJcIn0iLCAidHlwZSI6ICJydW4iLCAib3V0cHV0IjogInBkZiIsICJzdHJpcF9jb2RlIjogdHJ1ZSwgInJ1biI6ICJub3QgcnVuIiwgImNyZWF0ZWQiOiAiMTAvMzEvMjAxOCAxNjo0Mzo0NyIsICJtb2RpZmllZCI6ICIxMC8zMS8yMDE4IDE2OjQzOjQ3In19LCB7Im5hbWUiOiAiTXlKb2IyLVJlcG9ydC0yIiwgImlkIjogIlJlcG9ydC05IiwgIm1ldGEiOiB7Im5vdGVib29rIjogIk15Tm90ZWJvb2siLCAiam9iIjogIk15Sm9iMiIsICJwYXJhbWV0ZXJzIjogIntcInRpY2tlclwiOiBcIkdPT0dMXCJ9IiwgInR5cGUiOiAicnVuIiwgIm91dHB1dCI6ICJwZGYiLCAic3RyaXBfY29kZSI6IHRydWUsICJydW4iOiAibm90IHJ1biIsICJjcmVhdGVkIjogIjEwLzMxLzIwMTggMTY6NDM6NDciLCAibW9kaWZpZWQiOiAiMTAvMzEvMjAxOCAxNjo0Mzo0NyJ9fSwgeyJuYW1lIjogIk15Sm9iMi1SZXBvcnQtMyIsICJpZCI6ICJSZXBvcnQtMTAiLCAibWV0YSI6IHsibm90ZWJvb2siOiAiTXlOb3RlYm9vayIsICJqb2IiOiAiTXlKb2IyIiwgInBhcmFtZXRlcnMiOiAie1widGlja2VyXCI6IFwiSUJNXCJ9IiwgInR5cGUiOiAicnVuIiwgIm91dHB1dCI6ICJwZGYiLCAic3RyaXBfY29kZSI6IHRydWUsICJydW4iOiAibm90IHJ1biIsICJjcmVhdGVkIjogIjEwLzMxLzIwMTggMTY6NDM6NDciLCAibW9kaWZpZWQiOiAiMTAvMzEvMjAxOCAxNjo0Mzo0NyJ9fSwgeyJuYW1lIjogIk15Sm9iMi1SZXBvcnQtNCIsICJpZCI6ICJSZXBvcnQtMTEiLCAibWV0YSI6IHsibm90ZWJvb2siOiAiTXlOb3RlYm9vayIsICJqb2IiOiAiTXlKb2IyIiwgInBhcmFtZXRlcnMiOiAie1widGlja2VyXCI6IFwiTVNGVFwifSIsICJ0eXBlIjogInJ1biIsICJvdXRwdXQiOiAicGRmIiwgInN0cmlwX2NvZGUiOiB0cnVlLCAicnVuIjogIm5vdCBydW4iLCAiY3JlYXRlZCI6ICIxMC8zMS8yMDE4IDE2OjQzOjQ3IiwgIm1vZGlmaWVkIjogIjEwLzMxLzIwMTggMTY6NDM6NDcifX0sIHsibmFtZSI6ICJNeUpvYjItUmVwb3J0LTUiLCAiaWQiOiAiUmVwb3J0LTEyIiwgIm1ldGEiOiB7Im5vdGVib29rIjogIk15Tm90ZWJvb2siLCAiam9iIjogIk15Sm9iMiIsICJwYXJhbWV0ZXJzIjogIntcInRpY2tlclwiOiBcIk5GTFhcIn0iLCAidHlwZSI6ICJydW4iLCAib3V0cHV0IjogInBkZiIsICJzdHJpcF9jb2RlIjogdHJ1ZSwgInJ1biI6ICJub3QgcnVuIiwgImNyZWF0ZWQiOiAiMTAvMzEvMjAxOCAxNjo0Mzo0NyIsICJtb2RpZmllZCI6ICIxMC8zMS8yMDE4IDE2OjQzOjQ3In19XQ=='))


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
