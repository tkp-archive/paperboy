"""Copied from https://github.com/lwcolton/falcon-cors due to conda-forge issues.


                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "{}"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright {yyyy} {name of copyright owner}

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import re
import uuid

import mock
from nose.tools import raises

import falcon
from paperboy.middleware.cors import CORS
import falcon.testing as testing
from falcon.testing.resource import TestResource


class CORSResource(TestResource):
    def on_options(self, req, resp, **kwargs):
        self.req, self.resp, self.kwargs = req, resp, kwargs


class TestCors(testing.TestBase):
    def get_header(self, name):
        return self.resource.resp._headers.get(name.lower(), None)

    def get_rand_str(self):
        return str(uuid.uuid4())

    def simulate_cors_api(self, cors, route='/'):
        self.api = falcon.API(middleware=[cors.middleware])
        self.api.add_route(route, self.resource)

    @raises(ValueError)
    def test_init_settings(self):
        CORS(not_a_real_setting=True)

    @raises(ValueError)
    def test_init_allowed_methods(self):
        CORS(allow_methods_list=['not_a_real_method'])

    def test_vary_origins_true(self):
        cors = CORS(allow_all_origins=True, allow_credentials_origins_list=['test.com'])
        self.assertTrue(cors.origins_vary)

    def test_vary_origins_false(self):
        cors = CORS()
        self.assertFalse(cors.origins_vary)

    def test_compile_keys(self):
        regex_string = '.*'
        compiled_regex = re.compile(regex_string)
        test_compile_dict = {'some_regex': regex_string}
        cors = CORS()
        cors._compile_keys(test_compile_dict, ['some_regex'])
        self.assertEqual(compiled_regex, test_compile_dict['some_regex'])

    def simulate_cors_request(self, cors, route='/', preflight=False,
                              preflight_method='PATCH', add_request_method=True, **kwargs):
        self.resource = CORSResource()
        if preflight:
            kwargs.setdefault('headers', [])
            if add_request_method:
                kwargs['headers'].append(('access-control-request-method', preflight_method))
            method = 'OPTIONS'
        else:
            method = kwargs.pop('method', 'GET')

        self.simulate_cors_api(cors, route)
        self.simulate_request(route, method=method, **kwargs)

    def test_cors_disabled(self):
        self.resource = mock.MagicMock()
        self.resource.cors_enabled = False
        cors = CORS()
        cors.process = mock.Mock()
        self.simulate_cors_api(cors, '/')
        self.simulate_request('/', method='POST')
        self.assertEquals(cors.process.call_count, 0)

    def simulate_all_origins(self, preflight=False):
        cors_config = CORS(allow_all_origins=True, allow_methods_list=['PATCH'])
        origin = self.get_rand_str()
        headers = [('origin', origin)]
        self.simulate_cors_request(cors_config, headers=headers, preflight=preflight)
        self.assertEqual(self.get_header('access-control-allow-origin'), '*')
        self.assertEqual(self.get_header('access-control-allow-credentials'), None)

    def test_all_origins(self):
        self.simulate_all_origins()
        self.simulate_all_origins(preflight=True)

    def test_all_origins_credentials(self, preflight=False):
        cors_config = CORS(allow_all_origins=True, allow_credentials_all_origins=True,
                           allow_all_methods=True)
        origin = self.get_rand_str()
        headers = [('origin', origin)]
        self.simulate_cors_request(cors_config, headers=headers, preflight=preflight)
        self.assertEqual(self.get_header('access-control-allow-origin'), origin)
        self.assertEqual(self.get_header('access-control-allow-credentials'), 'true')

    def test_vary_origins_called(self):
        cors = CORS(allow_all_origins=True, allow_credentials_origins_list=['test.com'])
        cors._set_vary_origin = mock.Mock()
        origin = self.get_rand_str()
        headers = [('origin', origin)]
        self.simulate_cors_request(cors, headers=headers, preflight=False)
        cors._set_vary_origin.assert_called_once_with(self.resource.resp)

    def test_no_origin_return(self):
        cors = CORS()
        cors._process_origin = mock.Mock()
        self.simulate_cors_request(cors, preflight=False)
        self.assertEqual(cors._process_origin.call_count, 0)

    def test_process_origin_return(self):
        cors = CORS(allow_origins_list=['test.com'])
        cors._process_origin = mock.Mock(return_value=False)
        cors._process_credentials = mock.Mock()
        headers = [('origin', 'rackspace.com')]
        self.simulate_cors_request(cors, headers=headers, preflight=False)
        self.assertEqual(cors._process_origin.call_count, 1)
        self.assertEqual(cors._process_credentials.call_count, 0)

    def test_no_requested_method(self):
        cors = CORS(allow_all_origins=True)
        cors._get_requested_headers = mock.Mock()
        cors._process_origin = mock.Mock(return_value=True)
        headers = [('origin', 'rackspace.com')]
        self.simulate_cors_request(cors, headers=headers,
                                   preflight=True, add_request_method=False)
        self.assertEqual(cors._process_origin.call_count, 1)
        self.assertEqual(cors._get_requested_headers.call_count, 0)

    def test_method_not_allowed(self):
        cors = CORS(allow_all_origins=True, allow_methods_list=['GET'])
        cors._get_requested_headers = mock.Mock(return_value=True)
        cors._process_allow_headers = mock.Mock()
        headers = [('origin', 'rackspace.com')]
        self.simulate_cors_request(cors, headers=headers,
                                   preflight=True, preflight_method='POST')
        self.assertEqual(cors._get_requested_headers.call_count, 1)
        self.assertEqual(cors._process_allow_headers.call_count, 0)

    def test_header_not_allowed(self):
        cors = CORS(allow_all_origins=True, allow_all_methods=True,
                    allow_headers_list=['test_header'])
        cors._process_methods = mock.Mock(return_value=True)
        cors._process_credentials = mock.Mock()
        headers = [
            ('origin', 'rackspace.com'),
            ('access-control-request-headers', 'not_allowed_header')
        ]
        self.simulate_cors_request(cors, headers=headers, preflight=True)
        self.assertEqual(cors._process_methods.call_count, 1)
        self.assertEqual(cors._process_credentials.call_count, 0)

    def test_process_credentials_called(self):
        cors = CORS(allow_all_origins=True, allow_all_methods=True, allow_all_headers=True)
        cors._process_methods = mock.Mock(return_value=True)
        cors._process_credentials = mock.Mock()
        headers = [('origin', 'rackspace.com')]
        self.simulate_cors_request(cors, headers=headers, preflight=True)
        # print(cors._process_methods.call_count)
        cors._process_credentials.assert_called_once_with(
            self.resource.req,
            self.resource.resp,
            'rackspace.com'
        )

    def test_process_origin_allow_all(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        cors = CORS(allow_all_origins=True)
        cors._set_allow_origin = mock.Mock()
        self.assertEqual(
            cors._process_origin(fake_req, fake_resp, 'rackspace.com'),
            True
        )
        cors._set_allow_origin.assert_called_once_with(fake_resp, '*')
        cors._set_allow_origin = mock.Mock()
        cors.supports_credentials = True
        self.assertEqual(
            cors._process_origin(fake_req, fake_resp, 'rackspace.com'),
            True
        )
        cors._set_allow_origin.assert_called_once_with(fake_resp, 'rackspace.com')

    def test_process_origin_allow_list(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        cors = CORS(allow_origins_list=['rackspace.com'])
        cors._set_allow_origin = mock.Mock()
        self.assertEqual(
            cors._process_origin(fake_req, fake_resp, 'rackspace.com'),
            True
        )
        cors._set_allow_origin.assert_called_once_with(fake_resp, 'rackspace.com')

    def test_process_origin_allow_regex(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        cors = CORS(allow_origins_regex='rack.*\.com')
        cors._set_allow_origin = mock.Mock()
        self.assertEqual(
            cors._process_origin(fake_req, fake_resp, 'rackspace.com'),
            True
        )
        cors._set_allow_origin.assert_called_once_with(fake_resp, 'rackspace.com')

    def test_process_origin_regex_none(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        cors = CORS()
        cors._set_allow_origin = mock.Mock()
        self.assertEqual(
            cors._process_origin(fake_req, fake_resp, 'rackspace.com'),
            False
        )
        self.assertEqual(cors._set_allow_origin.call_count, 0)

    def test_process_origin_deny(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        cors = CORS(
            allow_origins_list=['rackspace.com'],
            allow_origins_regex='rack.*\.com'
        )
        cors._set_allow_origin = mock.Mock()
        self.assertEqual(
            cors._process_origin(fake_req, fake_resp, 'not_rackspace.com'),
            False
        )
        self.assertEqual(cors._set_allow_origin.call_count, 0)

    def test_process_allow_headers_all(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        cors = CORS(allow_all_headers=True)
        cors._set_allowed_headers = mock.Mock()
        self.assertEqual(
            cors._process_allow_headers(fake_req, fake_resp, ['test_header']),
            True
        )
        cors._set_allowed_headers.assert_called_once_with(fake_resp, ['test_header'])

    def test_process_allow_headers_list(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        cors = CORS(allow_headers_list=['test_header'])
        cors._set_allowed_headers = mock.Mock()
        self.assertEqual(
            cors._process_allow_headers(fake_req, fake_resp, ['test_header']),
            True
        )
        cors._set_allowed_headers.assert_called_once_with(fake_resp, ['test_header'])

    def test_process_allow_headers_list_camelcase(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        cors = CORS(allow_headers_list=['Content-Type'])
        cors._set_allowed_headers = mock.Mock()
        self.assertEqual(
            cors._process_allow_headers(fake_req, fake_resp, ['Content-Type']),
            True
        )
        cors._set_allowed_headers.assert_called_once_with(
            fake_resp, ['Content-Type']
        )

    def test_process_allow_headers_regex(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        cors = CORS(allow_headers_regex='.*_header')
        cors._set_allowed_headers = mock.Mock()
        self.assertEqual(
            cors._process_allow_headers(fake_req, fake_resp, ['test_header']),
            True
        )
        cors._set_allowed_headers.assert_called_once_with(fake_resp, ['test_header'])

    def test_process_allow_headers_disallow(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        cors = CORS(allow_headers_list=['test_header'], allow_headers_regex='.*_header')
        cors._set_allowed_headers = mock.Mock()
        self.assertEqual(
            cors._process_allow_headers(
                fake_req, fake_resp, ['test_header', 'header_not_allowed']
            ),
            False
        )
        self.assertEqual(cors._set_allowed_headers.call_count, 0)

    def test_process_methods_not_requested(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        fake_resource = mock.MagicMock()
        cors = CORS(allow_all_methods=True)
        cors._get_requested_method = mock.Mock(return_value=None)
        cors._set_allowed_methods = mock.Mock()
        self.assertEqual(
            cors._process_methods(fake_req, fake_resp, fake_resource),
            False
        )
        self.assertEqual(cors._set_allowed_methods.call_count, 0)
        cors._get_requested_method.assert_called_once_with(fake_req)

    def test_process_methods_allow_all_allowed(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        fake_resource = mock.MagicMock()
        cors = CORS(allow_all_methods=True)
        cors._get_requested_method = mock.Mock(return_value='GET')
        cors._get_resource_methods = mock.Mock(return_value=['GET', 'POST'])
        cors._set_allowed_methods = mock.Mock()
        self.assertEqual(
            cors._process_methods(fake_req, fake_resp, fake_resource),
            True
        )
        cors._set_allowed_methods.assert_called_once_with(fake_resp, ['GET', 'POST'])

    def test_process_methods_resource(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        fake_resource = mock.MagicMock()
        cors = CORS(allow_all_methods=True)
        cors._get_requested_method = mock.Mock(return_value='GET')
        cors._get_resource_methods = mock.Mock(return_value=['POST'])
        cors._set_allowed_methods = mock.Mock()
        self.assertEqual(
            cors._process_methods(fake_req, fake_resp, fake_resource),
            False
        )
        cors._set_allowed_methods.assert_called_once_with(fake_resp, ['POST'])

    def test_process_methods_allow_list(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        fake_resource = mock.MagicMock()
        cors = CORS(allow_methods_list=['GET', 'PUT', 'DELETE'])
        cors._set_allowed_methods = mock.Mock()
        cors._get_requested_method = mock.Mock(return_value='GET')
        cors._get_resource_methods = mock.Mock(return_value=['GET', 'POST', 'PUT'])
        self.assertEqual(
            cors._process_methods(fake_req, fake_resp, fake_resource),
            True
        )
        cors._set_allowed_methods.assert_called_once_with(fake_resp, ['GET', 'PUT'])

    def test_process_methods_notfound(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        fake_resource = mock.MagicMock()
        cors = CORS(allow_methods_list=['GET', 'POST', 'PUT', 'DELETE'])
        cors._set_allowed_methods = mock.Mock()
        cors._get_requested_method = mock.Mock(return_value='POST')
        cors._get_resource_methods = mock.Mock(return_value=['GET', 'PUT'])
        self.assertEqual(
            cors._process_methods(fake_req, fake_resp, fake_resource),
            False
        )
        cors._set_allowed_methods.assert_called_once_with(fake_resp, ['GET', 'PUT'])

    def test_process_credentials_all_origins(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        cors = CORS(allow_credentials_all_origins=True)
        cors._set_allow_credentials = mock.Mock()
        self.assertEqual(
            cors._process_credentials(fake_req, fake_resp, 'rackspace.com'),
            True
        )
        cors._set_allow_credentials.assert_called_once_with(fake_resp)

    def test_process_credentials_origins_list(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        cors = CORS(allow_credentials_origins_list=['rackspace.com'])
        cors._set_allow_credentials = mock.Mock()
        self.assertEqual(
            cors._process_credentials(fake_req, fake_resp, 'rackspace.com'),
            True
        )
        cors._set_allow_credentials.assert_called_once_with(fake_resp)

    def test_process_credentials_regex(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        cors = CORS(
            allow_credentials_origins_regex='.*\.rackspace\..*'
        )
        cors._set_allow_credentials = mock.Mock()
        self.assertEqual(
            cors._process_credentials(fake_req, fake_resp, 'www.rackspace.com'),
            True
        )
        cors._set_allow_credentials.assert_called_once_with(fake_resp)

    def test_process_credentials_disallow(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        cors = CORS(
            allow_credentials_origins_list=['not_rackspace'],
            allow_credentials_origins_regex='.*\.rackspace\..*'
        )
        cors._set_allow_credentials = mock.Mock()
        self.assertEqual(
            cors._process_credentials(fake_req, fake_resp, 'some_other_domain.lan'),
            False
        )
        self.assertEqual(cors._set_allow_credentials.call_count, 0)

    def test_process_expose_headers(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        cors = CORS(expose_headers_list=['test_header'])
        cors._process_expose_headers(fake_req, fake_resp)
        fake_resp.append_header.assert_called_once_with(
            'access-control-expose-headers', 'test_header'
        )

    def test_process_max_age(self):
        fake_req = mock.MagicMock()
        fake_resp = mock.MagicMock()
        cors = CORS(max_age=5)
        cors._process_max_age(fake_req, fake_resp)
        fake_resp.set_header.assert_called_once_with('access-control-max-age', 5)

    def test_set_allowed_headers(self):
        fake_resp = mock.MagicMock()
        allowed_header_list = ['header1']
        cors = CORS()
        cors._set_allowed_headers(fake_resp, allowed_header_list)
        fake_resp.append_header.assert_called_once_with('access-control-allow-headers', 'header1')

    def test_set_allowed_methods(self):
        fake_resp = mock.MagicMock()
        allowed_method_list = ['GET']
        cors = CORS()
        cors._set_allowed_methods(fake_resp, allowed_method_list)
        fake_resp.append_header.assert_called_once_with('access-control-allow-methods', 'GET')

    def test_set_very_origin(self):
        fake_resp = mock.MagicMock()
        cors = CORS()
        cors._set_vary_origin(fake_resp)
        fake_resp.append_header.assert_called_once_with('vary', 'origin')