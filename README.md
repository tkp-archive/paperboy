# paperboy
![Status](https://img.shields.io/badge/Status-BETA%201-yellow.svg?&longCache=true&style=for-the-badge)

A web frontend for scheduling Jupyter Notebooks as reports


# Overview

[![Build Status](https://travis-ci.org/timkpaine/paperboy.svg?branch=master)](https://travis-ci.org/timkpaine/paperboy)
![https://ci.appveyor.com/api/projects/status/32r7s2skrgm9ubva?svg=true](https://ci.appveyor.com/api/projects/status/32r7s2skrgm9ubva?svg=true)
[![Coverage](https://codecov.io/gh/timkpaine/paperboy/branch/master/graph/badge.svg)](https://codecov.io/gh/timkpaine/paperboy)
[![Docs](https://img.shields.io/readthedocs/paperboy.svg)](https://paperboy.readthedocs.io)
[![Site](https://img.shields.io/badge/Site--grey.svg?colorB=FFFFFF)](https://paperboy-jp.herokuapp.com/)

Paperboy is a production-grade application for scheduling reports. It has a flexible architecture and extensible APIs, and can integrate into a wide variety of deployments. It is composed of various industrial-strength technologies from the open source world.

- [Jupyter Notebooks](https://jupyter.org/documentation) for the reports themselves
    - Jupyter notebooks are an ideal report template, and with [NBConvert](https://github.com/jupyter/nbconvert) support a wide variety of output types, including PDFs, HTML, Emails, etc
- [Papermill](https://github.com/nteract/papermill) to parameterize notebooks
- [SQLAlchemy](https://www.sqlalchemy.org) for Storage (default)
- [Apache Airflow](https://airflow.apache.org) for Scheduling (default)
    - [Dask](https://dask.org) for [Airflow Workers](https://airflow.readthedocs.io/en/stable/howto/executor/use-dask.html)
    - [Luigi](https://luigi.readthedocs.io/en/stable/) as a scheduling alternative for `Airflow` (relies on `cron`) 
- [PhosphorJS](https://phosphorjs.github.io) for the frontend
- Support for Python [Virtualenvs](https://virtualenv.pypa.io/en/stable/) via `requirements.txt` or custom [Docker](https://www.docker.com) images via `Dockerfile`s on a per-notebook level
- Traitlets parameterization of storage and scheduler classes for easy integration with custom storage backends and custom schedulers
- Single click notebook deployment with [Voila](https://github.com/QuantStack/voila) and [Dokku](https://github.com/dokku/dokku)



![](https://raw.githubusercontent.com/timkpaine/paperboy/master/docs/img/ss.png)


## Process Flow
- Upload notebook
- Configure job
    - start time
    - interval
    - papermill parameters to autoconfigure reports
    - if autoconfiguring reports from papermill:
        - run or publish
        - output
            - notebook
            - pdf
            - html
            - email
            - script
        - strip or keep code
- To edit or create additional reports on a job, configure reports
    - run or publish
    - output
        - notebook
        - pdf
        - html
        - email
        - script
    - strip or keep code

# Installation from source

Paperboy requires Python and [Node.js](https://nodejs.org), which can be installed from `conda-forge` if `conda` is available.

Clone the repository and run following commands to install and launch the
application:

- npm install
- npm run build
- pip install -e .
- python -m paperboy

Visit http://0.0.0.0:8080 in a browser to view the application.

The default authentication backend requires the registration of a username that
can be used on subsequent launches.
