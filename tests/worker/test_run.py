import os
import os.path
from datetime import datetime
from paperboy.worker import run
from paperboy.config import NotebookConfig, NotebookMetadataConfig
from paperboy.config import JobConfig, JobMetadataConfig
from paperboy.config import ReportConfig, ReportMetadataConfig


class TestRun:
    def test_runlocal(self):
        os.environ['IEX_TOKEN'] = 'Tpk_ecc89ddf30a611e9958142010a80043c'
        os.makedirs(os.path.abspath(os.path.expanduser('~/Downloads')), exist_ok=True)

        now = datetime.now()

        notebook = NotebookConfig(name='MyNotebook',
                                  id='Notebook-1',
                                  meta=NotebookMetadataConfig(
                                    notebook='{\n "cells": [\n  {\n   "cell_type": "code",\n   "execution_count": null,\n   "metadata": {\n    "tags": [\n     "parameters"\n    ]\n   },\n   "outputs": [],\n   "source": [\n    "ticker = \'aapl\'"\n   ]\n  },\n  {\n   "cell_type": "code",\n   "execution_count": null,\n   "metadata": {},\n   "outputs": [],\n   "source": [\n    "ticker = ticker.upper()\\n",\n    "\\n",\n    "from IPython.display import HTML\\n",\n    "HTML(\'<h1>Report for {}</h1>\'.format(ticker))"\n   ]\n  },\n  {\n   "cell_type": "code",\n   "execution_count": null,\n   "metadata": {},\n   "outputs": [],\n   "source": [\n    "%matplotlib inline\\n",\n    "import pyEX\\n",\n "import pandas as pd\\n",\n    "import seaborn as sns\\n",\n    "\\n",\n    "sns.set()"\n   ]\n  },\n  {\n   "cell_type": "code",\n   "execution_count": null,\n   "metadata": {},\n   "outputs": [],\n   "source": [\n    "HTML(\'<h2>Performance</h2>\')"\n   ]\n  },\n  {\n   "cell_type": "code",\n   "execution_count": null,\n   "metadata": {},\n   "outputs": [],\n   "source": [\n    "c = pyEX.Client(\'Tpk_ecc89ddf30a611e9958142010a80043c\', version=\'sandbox\')\\n",\n    "df = c.chartDF(ticker)\\n",\n    "df[[\'open\', \'high\', \'low\', \'close\']].plot()"\n   ]\n  },\n  {\n   "cell_type": "code",\n   "execution_count": null,\n   "metadata": {},\n   "outputs": [],\n   "source": [\n    "HTML(\'<h2>Peer Correlation</h2>\')"\n   ]\n  },\n  {\n   "cell_type": "code",\n   "execution_count": null,\n   "metadata": {},\n   "outputs": [],\n   "source": [\n    "peers = c.peers(ticker)\\n",\n    "# doest work for test\\n",\n    "peers = [\'AAPL\', \'IBM\', \'NFLX\', \'MSFT\', \'INTC\']\\n",\n    "to_merge = {x: c.chartDF(x) for x in peers}\\n",\n    "to_merge.update({ticker: df})\\n",\n    "all = sorted(list(set(peers + [ticker])))\\n",\n    "rets = pd.concat(to_merge)\\n",\n    "rets = rets.unstack(0)[\'changePercent\'][all]\\n",\n    "rets = rets.corr()\\n",\n    "rets[\'symbol\'] = rets.index\\n",\n    "sns.heatmap(rets.corr())"\n   ]\n  },\n  {\n   "cell_type": "code",\n   "execution_count": null,\n   "metadata": {},\n   "outputs": [],\n   "source": []\n  }\n ],\n "metadata": {\n  "kernelspec": {\n   "display_name": "Python 3",\n   "language": "python",\n   "name": "python3"\n  },\n  "language_info": {\n   "codemirror_mode": {\n    "name": "ipython",\n    "version": 3\n   },\n   "file_extension": ".py",\n   "mimetype": "text/x-python",\n   "name": "python",\n   "nbconvert_exporter": "python",\n   "pygments_lexer": "ipython3",\n   "version": "3.7.3"\n  }\n },\n "nbformat": 4,\n "nbformat_minor": 4\n}'
                                  ),
                                  config=None
                                  )

        job = JobConfig(name='MyJob',
                        id='Job-1',
                        meta=JobMetadataConfig(
                            notebook=notebook,
                            interval='minutely',
                            level='production',
                            reports=6,
                            created=now,
                            modified=now,
                            config=None
                        ),
                        config=None
                        )

        reports = [
            ReportConfig(name='MyJob-Report-0',
                         id='Report-0',
                         meta=ReportMetadataConfig(notebook=notebook,
                                                   job=job,
                                                   parameters='{"ticker": "AAPL"}',
                                                   type='convert',
                                                   output='html',
                                                   strip_code=True,
                                                   template='',
                                                   created=now,
                                                   modified=now,
                                                   config=None
                                                   ),
                         config=None
                         )
        ]
        run(job, reports)
