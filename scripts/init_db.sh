#!/bin/bash
mkdir -p db
initdb -D db/ -A md5  -U airflow -W
echo "waiting for postgres to start"
. scripts/start_db.sh
airflow initdb