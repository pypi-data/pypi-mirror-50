# coding: utf-8

"""
/*
 Copyright 2019 IBM Corp.
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 */

"""

from __future__ import absolute_import

import unittest

import ibm_security_advisor_findings_api_client
from api.findings_graph_api import FindingsGraphApi  # noqa: E501
from ibm_security_advisor_findings_api_client.rest import ApiException


class TestFindingsGraphApi(unittest.TestCase):
    """FindingsGraphApi unit test stubs"""

    def setUp(self):
        self.api = api.findings_graph_api.FindingsGraphApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_post_graph(self):
        """Test case for post_graph

        query findings  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
