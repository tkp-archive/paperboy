import json
from base64 import b64decode
from paperboy.scheduler._airflow import JobOperator, JobCleanupOperator, ReportOperator, ReportPostOperator
from airflow import DAG
from datetime import timedelta, datetime


###################################
# Default arguments for operators #
###################################
default_args = {
    'owner': 'test',
    'start_date': datetime.strptime('10/30/2018 22:13:00', '%m/%d/%Y %H:%M:%S'),
    'email': ['test@test.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

###################################
# Inline job and reports as b64 json  #
###################################
job = json.loads(b64decode(b'eyJuYW1lIjogIk15Sm9iNCIsICJpZCI6ICJKb2ItNCIsICJtZXRhIjogeyJub3RlYm9vayI6ICJNeU5vdGVib29rIiwgImludGVydmFsIjogIm1pbnV0ZWx5IiwgImxldmVsIjogInByb2R1Y3Rpb24iLCAicmVwb3J0cyI6IDYsICJjcmVhdGVkIjogIjEwLzMwLzIwMTggMTg6MTM6NTQiLCAibW9kaWZpZWQiOiAiMTAvMzAvMjAxOCAxODoxMzo1NCJ9fQ=='))
reports = json.loads(b64decode(b'W3sibmFtZSI6ICJNeUpvYjQtUmVwb3J0LTAiLCAiaWQiOiAiUmVwb3J0LU5vbmUiLCAibWV0YSI6IHsibm90ZWJvb2siOiAiTXlOb3RlYm9vayIsICJqb2IiOiAiTXlKb2I0IiwgInBhcmFtZXRlcnMiOiAie1widGlja2VyXCI6IFwiQUFQTFwifSIsICJ0eXBlIjogInJ1biIsICJvdXRwdXQiOiAibm90ZWJvb2siLCAic3RyaXBfY29kZSI6IHRydWUsICJydW4iOiAibm90IHJ1biIsICJjcmVhdGVkIjogIjEwLzMwLzIwMTggMTg6MTM6NTQiLCAibW9kaWZpZWQiOiAiMTAvMzAvMjAxOCAxODoxMzo1NCJ9fSwgeyJuYW1lIjogIk15Sm9iNC1SZXBvcnQtMSIsICJpZCI6ICJSZXBvcnQtTm9uZSIsICJtZXRhIjogeyJub3RlYm9vayI6ICJNeU5vdGVib29rIiwgImpvYiI6ICJNeUpvYjQiLCAicGFyYW1ldGVycyI6ICJ7XCJ0aWNrZXJcIjogXCJGQlwifSIsICJ0eXBlIjogInJ1biIsICJvdXRwdXQiOiAibm90ZWJvb2siLCAic3RyaXBfY29kZSI6IHRydWUsICJydW4iOiAibm90IHJ1biIsICJjcmVhdGVkIjogIjEwLzMwLzIwMTggMTg6MTM6NTQiLCAibW9kaWZpZWQiOiAiMTAvMzAvMjAxOCAxODoxMzo1NCJ9fSwgeyJuYW1lIjogIk15Sm9iNC1SZXBvcnQtMiIsICJpZCI6ICJSZXBvcnQtTm9uZSIsICJtZXRhIjogeyJub3RlYm9vayI6ICJNeU5vdGVib29rIiwgImpvYiI6ICJNeUpvYjQiLCAicGFyYW1ldGVycyI6ICJ7XCJ0aWNrZXJcIjogXCJHT09HTFwifSIsICJ0eXBlIjogInJ1biIsICJvdXRwdXQiOiAibm90ZWJvb2siLCAic3RyaXBfY29kZSI6IHRydWUsICJydW4iOiAibm90IHJ1biIsICJjcmVhdGVkIjogIjEwLzMwLzIwMTggMTg6MTM6NTQiLCAibW9kaWZpZWQiOiAiMTAvMzAvMjAxOCAxODoxMzo1NCJ9fSwgeyJuYW1lIjogIk15Sm9iNC1SZXBvcnQtMyIsICJpZCI6ICJSZXBvcnQtTm9uZSIsICJtZXRhIjogeyJub3RlYm9vayI6ICJNeU5vdGVib29rIiwgImpvYiI6ICJNeUpvYjQiLCAicGFyYW1ldGVycyI6ICJ7XCJ0aWNrZXJcIjogXCJJQk1cIn0iLCAidHlwZSI6ICJydW4iLCAib3V0cHV0IjogIm5vdGVib29rIiwgInN0cmlwX2NvZGUiOiB0cnVlLCAicnVuIjogIm5vdCBydW4iLCAiY3JlYXRlZCI6ICIxMC8zMC8yMDE4IDE4OjEzOjU0IiwgIm1vZGlmaWVkIjogIjEwLzMwLzIwMTggMTg6MTM6NTQifX0sIHsibmFtZSI6ICJNeUpvYjQtUmVwb3J0LTQiLCAiaWQiOiAiUmVwb3J0LU5vbmUiLCAibWV0YSI6IHsibm90ZWJvb2siOiAiTXlOb3RlYm9vayIsICJqb2IiOiAiTXlKb2I0IiwgInBhcmFtZXRlcnMiOiAie1widGlja2VyXCI6IFwiTVNGVFwifSIsICJ0eXBlIjogInJ1biIsICJvdXRwdXQiOiAibm90ZWJvb2siLCAic3RyaXBfY29kZSI6IHRydWUsICJydW4iOiAibm90IHJ1biIsICJjcmVhdGVkIjogIjEwLzMwLzIwMTggMTg6MTM6NTQiLCAibW9kaWZpZWQiOiAiMTAvMzAvMjAxOCAxODoxMzo1NCJ9fSwgeyJuYW1lIjogIk15Sm9iNC1SZXBvcnQtNSIsICJpZCI6ICJSZXBvcnQtTm9uZSIsICJtZXRhIjogeyJub3RlYm9vayI6ICJNeU5vdGVib29rIiwgImpvYiI6ICJNeUpvYjQiLCAicGFyYW1ldGVycyI6ICJ7XCJ0aWNrZXJcIjogXCJORkxYXCJ9IiwgInR5cGUiOiAicnVuIiwgIm91dHB1dCI6ICJub3RlYm9vayIsICJzdHJpcF9jb2RlIjogdHJ1ZSwgInJ1biI6ICJub3QgcnVuIiwgImNyZWF0ZWQiOiAiMTAvMzAvMjAxOCAxODoxMzo1NCIsICJtb2RpZmllZCI6ICIxMC8zMC8yMDE4IDE4OjEzOjU0In19XQ=='))


###################################
# Create dag from job and reports #
###################################

# The top level dag, representing a Job run on a Notebook
dag = DAG('DAG_' + str(job['id']), default_args=default_args)

# The Job operator, used for bundling groups of reports,
# setting up env/image
job = JobOperator(task_id=job['id'], dag=dag)

# The cleanup operator, run after all reports are finished
cleanup = JobCleanupOperator(task_id='job_cleanup', dag=dag)

for rep in reports:
    # Report operator, performs the report creation
    # using papermill and the report's individual
    # parameters and configuration
    r = ReportOperator(task_id=rep['id'], dag=dag)

    # The post-report operator, used for post-report
    # tasks such as sending the report in an email,
    # deploying the report to a webserver, etc
    rp = ReportPostOperator(task_id=rep['id'], dag=dag)

    # Job -> Report -> ReportPost -\
    #   \--> Report -> ReportPost --\
    #    \-> Report -> ReportPost ----> Job Cleanup
    job.set_downstream(r)
    r.set_downstream(rp)
    rp.set_downstream(cleanup)
