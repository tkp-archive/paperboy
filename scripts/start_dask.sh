#!/bin/bash
DASK_HOST=127.0.0.1
DASK_PORT=8786
BOKEH_PORT=8787

dask-scheduler --host $DASK_HOST --port $DASK_PORT --bokeh-port $BOKEH_PORT
