# paperboy
A web frontend for scheduling notebooks

[![Build Status](https://travis-ci.org/timkpaine/paperboy.svg?branch=master)](https://travis-ci.org/timkpaine/paperboy)
[![Waffle.io](https://badge.waffle.io/timkpaine/paperboy.png?label=ready&title=Ready)](https://waffle.io/timkpaine/paperboy?utm_source=badge)
[![Coverage](https://codecov.io/gh/timkpaine/paperboy/branch/master/graph/badge.svg)](https://codecov.io/gh/timkpaine/paperboy)
[![Docs](https://img.shields.io/readthedocs/paperboy.svg)](https://paperboy.readthedocs.io)


[Link](https://paperboy-jp.herokuapp.com/)

# Overview
Paperboy is a production-grade application for scheduling reports. It has a flexible architecture and extensible APIs, and can integrate into a wide variety of deployments. It is composed of various industrial-strength technologies from the open source world.

- Jupyter Notebooks for the reports themselves
    - Jupyter notebooks are an ideal report template, and with NBConvert support a wide variety of output types, including PDFs, HTML, Emails, etc
- SQLAlchemy for Storage
- Apache Airflow for Scheduling
- PhosphorJS for the frontend


Some future options include:

- MongoDB storage
- Luigi scheduler


## Arch
![](https://raw.githubusercontent.com/timkpaine/paperboy/master/docs/arch.png)
