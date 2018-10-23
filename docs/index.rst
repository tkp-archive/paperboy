.. paperboy documentation master file, created by
   sphinx-quickstart on Fri Jan 12 22:07:11 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
paperboy
========

A web frontend for scheduling Jupyter Notebooks as reports

|Build Status| |Waffle.io| |Coverage| |Docs| |Site|

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart


Overview
========

Paperboy is a production-grade application for scheduling reports. It
has a flexible architecture and extensible APIs, and can integrate into
a wide variety of deployments. It is composed of various
industrial-strength technologies from the open source world.

-  `Jupyter Notebooks <https://jupyter.org/documentation>`__ for the
   reports themselves

   -  Jupyter notebooks are an ideal report template, and with
      `NBConvert <https://github.com/jupyter/nbconvert>`__ support a
      wide variety of output types, including PDFs, HTML, Emails, etc

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

|image5|

Arch
----

|image6|

.. |Build Status| image:: https://travis-ci.org/timkpaine/paperboy.svg?branch=master
   :target: https://travis-ci.org/timkpaine/paperboy
.. |Waffle.io| image:: https://badge.waffle.io/timkpaine/paperboy.png?label=ready&title=Ready
   :target: https://waffle.io/timkpaine/paperboy?utm_source=badge
.. |Coverage| image:: https://codecov.io/gh/timkpaine/paperboy/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/timkpaine/paperboy
.. |Docs| image:: https://img.shields.io/readthedocs/paperboy.svg
   :target: https://paperboy.readthedocs.io
.. |Site| image:: https://img.shields.io/badge/Site--grey.svg?colorB=FFFFFF
   :target: https://paperboy-jp.herokuapp.com/
.. |image5| image:: https://raw.githubusercontent.com/timkpaine/paperboy/master/docs/ss.png
.. |image6| image:: https://raw.githubusercontent.com/timkpaine/paperboy/master/docs/arch.png

