###############################
# Remote Airflow              #
# This is used when running   #
# airflow on a remote machine #
###############################
import falcon
import json
import logging
from paperboy.server.deploy import FalconDeploy
from six.moves.urllib_parse import urljoin


class RemoteAirflowResource(object):
    def __init__(self):
        pass

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({'test': 'ok'})

    def on_post(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({'test': 'ok'})


class RemoteAirflowStatusResource(object):
    def __init__(self):
        pass

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({'test': 'ok'})

    def on_post(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps({'test': 'ok'})


def main(baseurl='/'):
    def from_base(url):
        return urljoin(baseurl, url)

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

if __name__ == '__main__':
    main()
