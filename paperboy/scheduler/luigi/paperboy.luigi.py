# This is the jinja2 templatized set of tasks that
# generates the job. It has the following form as an
# example:
#
#    Job -> Report -> Papermill -> NBConvert ->      ReportPost -\
#      \--> Report -> Papermill -> Voila -> Dokku -> ReportPost --\
#       \-> Report -> Papermill -> NBConvert ->      ReportPost ----> Job Cleanup
#

import json
from base64 import b64decode

# Base Job Tasks
from paperboy.scheduler.luigi_tasks import JobTask, JobCleanupTask

# Base Report Tasks
from paperboy.scheduler.luigi_tasks import ReportTask, ReportPostTask

# Convert Tasks
from paperboy.scheduler.luigi_tasks import PapermillTask, NBConvertTask

# Publish operators
from paperboy.scheduler.luigi_tasks import VoilaTask, DokkuTask

from datetime import datetime

###################################
# Inline job and reports as b64 json  #
###################################
job_json = json.loads(b64decode({{job_json}}))
reports_json = json.loads(b64decode({{report_json}}))

interval = "{{interval}}"
start_date = datetime.strptime('{{start_date}}', '%m/%d/%Y %H:%M:%S')
owner = "{{owner}}"
email = "{{email}}"

###################################
# Create dag from job and reports #
###################################

# The Job task, used for bundling groups of reports,
# setting up env/image
job = JobTask(job=job_json,
              task_id='Job-{}'.format(job_json['id']),
              requires=[],
              owner=owner,
              start_date=start_date,
              interval=interval,
              email=email)

cleanup_requires = []

for rep in reports_json:
    # copy over notebook text (only store 1 copy in the job json)
    rep['meta']['notebook_text'] = job_json['meta']['notebook_text']

    # type is "convert" for nbconversion jobs and "publish" for publish jobs
    type = rep['meta']['type']

    # Report task, performs the required
    # steps prior to running the report
    r = ReportTask(report=rep,
                   task_id='Report-{}'.format(rep['id']),
                   requires=[job],
                   owner=owner,
                   start_date=start_date,
                   interval=interval,
                   email=email)

    # Papermill task, performs the report creation
    # using papermill and the report's individual
    # parameters and configuration
    pp = PapermillTask(report=rep,
                       task_id='ReportPapermill-{}'.format(rep['id']),
                       requires=[r],
                       owner=owner,
                       start_date=start_date,
                       interval=interval,
                       email=email)

    if type == 'convert':
        # NBConvert task, performs the NBConversion if
        # required
        nb = NBConvertTask(report=rep,
                           task_id='ReportNBConvert-{}'.format(rep['id']),
                           requires=[pp],
                           owner=owner,
                           start_date=start_date,
                           interval=interval,
                           email=email)

    elif type == 'publish':
        # Dokku deployment task, performs the
        # deploy to the dokku repo
        d = DokkuTask(report=rep,
                      task_id='ReportDokku-{}'.format(rep['id']),
                      requires=[pp],
                      owner=owner,
                      start_date=start_date,
                      interval=interval,
                      email=email)

        # Assemble a Voila Job from papermilled notebook
        nb = VoilaTask(report=rep,
                       task_id='ReportVoila-{}'.format(rep['id']),
                       requires=[d],
                       owner=owner,
                       start_date=start_date,
                       interval=interval,
                       email=email)

    else:
        raise NotImplementedError()


# The post-report task, used for post-report
# tasks such as sending the report in an email
# or pushing the deploy to dokku
rp = ReportPostTask(report=rep,
                    config=json.loads('{{output_config}}'),
                    task_id='ReportPost-{}'.format(rep['id']),
                    requires=cleanup_requires,
                    owner=owner,
                    start_date=start_date,
                    interval=interval,
                    email=email)

# The cleanup task, run after all reports are finished
cleanup = JobCleanupTask(job=job_json,
                         task_id='JobCleanup-{}'.format(job_json['id']),
                         requires=[rp],
                         owner=owner,
                         start_date=start_date,
                         interval=interval,
                         email=email)
