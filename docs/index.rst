.. paperboy documentation master file, created by
   sphinx-quickstart on Fri Jan 12 22:07:11 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

paperboy
========

.. figure:: https://img.shields.io/badge/Status-BETA%201-yellow.svg?&longCache=true&style=for-the-badge
   :alt: Status

A web frontend for scheduling Jupyter Notebooks as reports


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   architecture
   api


Overview
========

|Build Status|
|https://ci.appveyor.com/api/projects/status/32r7s2skrgm9ubva?svg=true|
|Coverage| |Docs| |Site|

Paperboy is a production-grade application for scheduling reports. It
has a flexible architecture and extensible APIs, and can integrate into
a wide variety of deployments. It is composed of various
industrial-strength technologies from the open source world.

-  `Jupyter Notebooks <https://jupyter.org/documentation>`__ for the
   reports themselves

   -  Jupyter notebooks are an ideal report template, and with
      `NBConvert <https://github.com/jupyter/nbconvert>`__ support a
      wide variety of output types, including PDFs, HTML, Emails, etc

-  `Papermill <https://github.com/nteract/papermill>`__ to parameterize
   notebooks
-  `SQLAlchemy <https://www.sqlalchemy.org>`__ for Storage
-  `Apache Airflow <https://airflow.apache.org>`__ for Scheduling
-  `Dask <https://dask.org>`__ for `Airflow
   Workers <https://airflow.readthedocs.io/en/stable/howto/executor/use-dask.html>`__
-  `Kubernetes <https://kubernetes.io>`__ for worker instances
-  `PhosphorJS <https://phosphorjs.github.io>`__ for the frontend
-  Support for Python
   `Virtualenvs <https://virtualenv.pypa.io/en/stable/>`__ via
   ``requirements.txt`` or custom `Docker <https://www.docker.com>`__
   images via ``Dockerfile``\ s on a per-notebook level

Some future options include:

-  MongoDB storage
-  Luigi scheduler

|image6|

Process Flow
------------

-  Upload notebook
-  Configure job

   -  start time
   -  interval
   -  papermill parameters to autoconfigure reports
   -  if autoconfiguring reports from papermill:

      -  run or publish
      -  output

         -  notebook
         -  pdf
         -  html
         -  email
         -  script

      -  strip or keep code

-  To edit or create additional reports on a job, configure reports

   -  run or publish
   -  output

      -  notebook
      -  pdf
      -  html
      -  email
      -  script

   -  strip or keep code


Installation from source
--------------------------

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

.. |Build Status| image:: https://travis-ci.org/timkpaine/paperboy.svg?branch=master
   :target: https://travis-ci.org/timkpaine/paperboy
.. |https://ci.appveyor.com/api/projects/status/32r7s2skrgm9ubva?svg=true| image:: https://ci.appveyor.com/api/projects/status/32r7s2skrgm9ubva?svg=true
.. |Coverage| image:: https://codecov.io/gh/timkpaine/paperboy/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/timkpaine/paperboy
.. |Docs| image:: https://img.shields.io/readthedocs/paperboy.svg
   :target: https://paperboy.readthedocs.io
.. |Site| image:: https://img.shields.io/badge/Site--grey.svg?colorB=FFFFFF
   :target: https://paperboy-jp.herokuapp.com/
.. |image6| image:: ./img/ss.png
