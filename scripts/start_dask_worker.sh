#!/bin/bash
DASK_HOST=127.0.0.1
DASK_PORT=8786

# on a worker machine
dask-worker $DASK_HOST:$DASK_PORT
