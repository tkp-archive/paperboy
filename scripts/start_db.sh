#!/bin/bash
pg_ctl -D db -l logfile start
createdb -O airflow airflow -E utf-8 -U airflow -p 5432
