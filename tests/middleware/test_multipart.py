"""Copied from https://github.com/yohanboniface/falcon-multipart due to conda-forge issues.

MIT License

Copyright (c) 2017 Yohan Boniface

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from io import open
import os

import falcon
from paperboy.middleware import MultipartMiddleware
import pytest


application = falcon.API(middleware=MultipartMiddleware())


@pytest.fixture
def app():
    return application


def test_parse_form_as_params(client):

    class Resource:

        def on_post(self, req, resp, **kwargs):
            assert req.get_param('simple') == 'ok'
            assert req.get_param('afile').file.read() == b'filecontent'
            assert req.get_param('afile').filename == 'afile.txt'
            resp.body = 'parsed'
            resp.content_type = 'text/plain'

    application.add_route('/route', Resource())

    resp = client.post('/route', data={'simple': 'ok'},
                       files={'afile': ('filecontent', 'afile.txt')})
    assert resp.status == falcon.HTTP_OK
    assert resp.body == 'parsed'


def test_with_binary_file(client):
    here = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(here, 'image.jpg')
    image = open(filepath, 'rb')

    class Resource:

        def on_post(self, req, resp, **kwargs):
            resp.data = req.get_param('afile').file.read()
            resp.content_type = 'image/jpg'

    application.add_route('/route', Resource())

    resp = client.post('/route', data={'simple': 'ok'},
                       files={'afile': image})
    assert resp.status == falcon.HTTP_OK
    image.seek(0)
    assert resp.body == image.read()


def test_parse_multiple_values(client):

    class Resource:

        def on_post(self, req, resp, **kwargs):
            assert req.get_param_as_list('multi') == ['1', '2']
            resp.body = 'parsed'
            resp.content_type = 'text/plain'

    application.add_route('/route', Resource())

    resp = client.post('/route', data={'multi': ['1', '2']},
                       files={'afile': ('filecontent', 'afile.txt')})
    assert resp.status == falcon.HTTP_OK
    assert resp.body == 'parsed'


def test_parse_non_ascii_filename_in_headers(client):

    class Resource:

        def on_post(self, req, resp, **kwargs):
            assert req.get_param('afile').file.read() == b'name,code\nnom,2\n'
            assert req.get_param('afile').filename == 'Na%C3%AFve%20file.txt'
            resp.body = 'parsed'
            resp.content_type = 'text/plain'

    application.add_route('/route', Resource())

    # Simulate browser sending non ascii filename.
    body = ('--boundary\r\nContent-Disposition: '
            'form-data; name="afile"; filename*=utf-8\'\'Na%C3%AFve%20file.txt'
            '\r\nContent-Type: text/csv\r\n\r\nname,code\nnom,2\n\r\n'
            '--boundary--\r\n')
    headers = {'Content-Type': 'multipart/form-data; boundary=boundary'}
    resp = client.post('/route', body=body, headers=headers)
    assert resp.status == falcon.HTTP_OK
    assert resp.body == 'parsed'
