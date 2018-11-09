
# Contributing

## Setting up a development environment
The easiest way to get started is to clone the repository locally. If `paperboy.db` exists, simply delete it, this is my debug database. In the `Makefile` you'll see the `runsql` target. This runs with sql authentication, and a sqlite backend. Run it by running `python3 -m paperboy.server --backend='sqla' --auth='sqla'`

Navigate to port `8080`. At the login screen, simply click `Register` and choose any username. There is no password with dummy auth.

![](https://raw.githubusercontent.com/timkpaine/paperboy/master/docs/img/contributing1.png)

## Getting running
Navigate to the `Notebooks` tab, then the uploader, and upload a notebook of your choice (I recommend `examples/sample.ipynb` included in this repo.

![](https://raw.githubusercontent.com/timkpaine/paperboy/master/docs/img/contributing2.png)
![](https://raw.githubusercontent.com/timkpaine/paperboy/master/docs/img/contributing3.gif)

From there, you can start to setup jobs, which will dump `Airflow` compatible DAGs into `~/airflow/dags` by default.

Navigate to the `Jobs` tab to add your first job. As an example, we will configure the `sample.ipynb` notebook to run with the papermill parameters defined in `examples/params_min.jsonl`.

![](https://raw.githubusercontent.com/timkpaine/paperboy/master/docs/img/contributing4.png)
![](https://raw.githubusercontent.com/timkpaine/paperboy/master/docs/img/contributing5.gif)


Since the `autogen reports` checkbox was full, we autogenerate 6 reports corresonding to the 6 different parameters in the file. As a result, you should now see these in the reports tab:

![](https://raw.githubusercontent.com/timkpaine/paperboy/master/docs/img/contributing6.png)

You should also see a new dag in `~/airflow/dags`, and the dag in the airflow UI. If airflow is configured to start dags automatically, you will soon see 6 reports in `~/Downloads` every minute until you halt the job. 

![](https://raw.githubusercontent.com/timkpaine/paperboy/master/docs/img/dag.png)
