===============

Getting started
===============

Setup
------
The quickest way to get up and running is to install paperboy and its default requirements

.. code:: bash

    pip install paperboy

And then to run the paperboy server without authentication against a "fale" airflow scheduler and with SQLite in-memory as the storage backend

.. code:: bash

    python3 -m paperboy.server


Configuring with SQLAlchemy
----------------------------
Paperboy can be easily configured to run using SQLAlchemy for storage and authentication.

.. code:: bash

    python3 -m paperboy.server --backend='sqla' --auth='sqla'



Configuring with Airflow
--------------------------
Paperboy's default scheduler is Apache Airflow. As such it will generate DAGs and place them into a specified folder, where they can be consumed by Airflow. It will generate and run commands to manage the lifecycle of jobs and reports as well, including adding/deleting/querying airflow via its command line interface.


Overview
===============
Paperboy is built around traitlets, and is designed to be easily extendable and integrateable with various schedulers, authentication, and storage backends. This is done intentionally for flexibility when integrating with proprietary internal systems. 


Storage Backend
------------------

Authentication Backend
-----------------------

Scheduler Backend
-----------------------
