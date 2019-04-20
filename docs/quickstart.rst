===============

Getting started
===============

Setup
------
The quickest way to get up and running is to install paperboy and its default requirements

.. code:: bash

    pip install paperboy

And then to run the paperboy server without authentication against a "fale" airflow scheduler and with sqlite as the storage backend

.. code:: bash

    python3 -m paperboy.server


Configuring with SQLAlchemy
----------------------------


Configuring with Airflow
--------------------------



Overview
===============
Paperboy is built around traitlets, and is designed to be easily extendable and integrateable with various schedulers, authentication, and storage backends. This is done intentionally for flexibility when integrating with proprietary internal systems. 


Storage Backend
------------------

Authentication Backend
-----------------------

Scheduler Backend
-----------------------
