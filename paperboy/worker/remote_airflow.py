###############################
# Remote Airflow              #
# This is used when running   #
# airflow on a remote machine #
###############################
import falcon
import json
import logging
import os
from paperboy.server.deploy import FalconDeploy
from paperboy.config.scheduler import AirflowSchedulerConfig
from paperboy.scheduler.airflow import AirflowScheduler
from six.moves.urllib_parse import urljoin
from traitlets.config.application import Application
from traitlets import Int, Unicode


class RemoteAirflow(Application):
    name = 'remoteairflow'
    description = 'remoteairflow'

    ############
    # Gunicorn #
    ############
    workers = Int(default_value=1, help="Number of gunicorn workers").tag(config=True)
    port = Unicode(default_value='8080', help="Port to run on").tag(config=True)
    ############

    #############
    # Scheduler #
    #############
    # FIXME doesnt allow default_value yet
    scheduler = AirflowSchedulerConfig()
    #############

    def start(self):
        """Start the whole thing"""
        self.port = os.environ.get('PORT', self.port)
        options = {
            'bind': '0.0.0.0:{}'.format(self.port),
            'workers': self.workers
        }

        def from_base(url):
            return urljoin(self.baseurl, url)

        api = falcon.API()

        remote = RemoteAirflowResource()
        status = RemoteAirflowStatusResource()
        api.add_route(from_base('remote'), remote)
        api.add_route(from_base('status'), status)

        ##########
        port = 8081
        options = {
            'bind': '0.0.0.0:{}'.format(port),
            'workers': 1
        }
        logging.debug('Running on port:{}'.format(port))
        FalconDeploy(api, options).run()

    @classmethod
    def launch_instance(cls, argv=None, **kwargs):
        """Launch an instance of a Paperboy Application"""
        return super(RemoteAirflow, cls).launch_instance(argv=argv, **kwargs)

    aliases = {
        'workers': 'RemoteAirflow.workers',
        'port': 'RemoteAirflow.port',
        'baseurl': 'RemoteAirflow.baseurl',
    }


class RemoteAirflowResource(object):
    def __init__(self):
        pass

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({'status': 'ok'})

    def on_post(self, req, resp):
        template = req.params['template']
        name = req.params['name']
        with open(os.path.join(self.config.scheduler.dagbag, name), 'w') as fp:
            fp.write(template)

        resp.content_type = 'application/json'
        resp.body = json.dumps({'status': 'ok'})


class RemoteAirflowStatusResource(object):
    def __init__(self):
        pass

    def on_get(self, req, resp):
        # TODO pull status args out of request
        engine = req.params.get('engine')
        type = req.params.get('type', '')
        if not self.sql_conn:
            gen = AirflowScheduler.fakequery(engine)
            if type == 'jobs':
                ret = gen['jobs']
            elif type == 'reports':
                ret = gen['reports']
            else:
                ret = gen
        else:
            gen = AirflowScheduler.query(engine)
            if type == 'jobs':
                ret = gen['jobs']
            elif type == 'reports':
                ret = gen['reports']
            else:
                ret = gen

        resp.content_type = 'application/json'
        resp.body = json.dumps(ret)

    def on_post(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({'status': 'ok'})


if __name__ == '__main__':
    RemoteAirflow.launch_instance()
