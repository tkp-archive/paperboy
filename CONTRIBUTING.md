
# Contributing

## Setting up a development environment
The easiest way to get started is to clone the repository locally. If `paperboy.db` exists, simply delete it, this is my debug database. In the `Makefile` you'll see the `runsql` target. This runs with sql authentication, and a sqlite backend. Run it by running `python3 -m paperboy.server --backend='sqla' --auth='sqla'`

Navigate to port `8080`. At the login screen, simply click `Register` and choose any username. There is no password with dummy auth.

![](https://raw.githubusercontent.com/timkpaine/paperboy/master/docs/img/contributing1.png)

## Getting running
Navigate to the `Notebooks` tab, then the uploader, and upload a notebook of your choice (I recommend `examples/sample.ipynb` included in this repo.

From there, you can start to setup jobs, which will dump `Airflow` compatible DAGs into `~/airflow/dags` by default.

![](https://raw.githubusercontent.com/timkpaine/paperboy/master/docs/img/contributing2.png)



Under construction...
