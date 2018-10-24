# paperboy
A web frontend for scheduling Jupyter Notebooks as reports

[![Build Status](https://travis-ci.org/timkpaine/paperboy.svg?branch=master)](https://travis-ci.org/timkpaine/paperboy)
[![Waffle.io](https://badge.waffle.io/timkpaine/paperboy.png?label=ready&title=Ready)](https://waffle.io/timkpaine/paperboy?utm_source=badge)
[![Coverage](https://codecov.io/gh/timkpaine/paperboy/branch/master/graph/badge.svg)](https://codecov.io/gh/timkpaine/paperboy)
[![Docs](https://img.shields.io/readthedocs/paperboy.svg)](https://paperboy.readthedocs.io)
[![Site](https://img.shields.io/badge/Site--grey.svg?colorB=FFFFFF)](https://paperboy-jp.herokuapp.com/)

# Overview
Paperboy is a production-grade application for scheduling reports. It has a flexible architecture and extensible APIs, and can integrate into a wide variety of deployments. It is composed of various industrial-strength technologies from the open source world.

- [Jupyter Notebooks](https://jupyter.org/documentation) for the reports themselves
    - Jupyter notebooks are an ideal report template, and with [NBConvert](https://github.com/jupyter/nbconvert) support a wide variety of output types, including PDFs, HTML, Emails, etc
- [Papermill](https://github.com/nteract/papermill) to parameterize notebooks
- [SQLAlchemy](https://www.sqlalchemy.org) for Storage
- [Apache Airflow](https://airflow.apache.org) for Scheduling
- [Dask](https://dask.org) for [Airflow Workers](https://airflow.readthedocs.io/en/stable/howto/executor/use-dask.html)
- [Kubernetes](https://kubernetes.io) for worker instances
- [PhosphorJS](https://phosphorjs.github.io) for the frontend
- Support for Python [Virtualenvs](https://virtualenv.pypa.io/en/stable/) via `requirements.txt` or custom [Docker](https://www.docker.com) images via `Dockerfile`s on a per-notebook level


Some future options include:

- MongoDB storage
- Luigi scheduler

![](https://raw.githubusercontent.com/timkpaine/paperboy/master/docs/ss.png)


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

## Storage Arch
![](https://raw.githubusercontent.com/timkpaine/paperboy/master/docs/arch.png)
