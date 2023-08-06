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
from api.findings_occurrences_api import FindingsOccurrencesApi  # noqa: E501
from ibm_security_advisor_findings_api_client.rest import ApiException


class TestFindingsOccurrencesApi(unittest.TestCase):
    """FindingsOccurrencesApi unit test stubs"""

    def setUp(self):
        self.api = api.findings_occurrences_api.FindingsOccurrencesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_occurrence(self):
        """Test case for create_occurrence

        Creates a new `Occurrence`. Use this method to create `Occurrences` for a resource.  # noqa: E501
        """
        pass

    def test_delete_occurrence(self):
        """Test case for delete_occurrence

        Deletes the given `Occurrence` from the system.  # noqa: E501
        """
        pass

    def test_get_occurrence(self):
        """Test case for get_occurrence

        Returns the requested `Occurrence`.  # noqa: E501
        """
        pass

    def test_list_note_occurrences(self):
        """Test case for list_note_occurrences

        Lists `Occurrences` referencing the specified `Note`. Use this method to get all occurrences referencing your `Note` across all your customer providers.  # noqa: E501
        """
        pass

    def test_list_occurrences(self):
        """Test case for list_occurrences

        Lists active `Occurrences` for a given provider matching the filters.  # noqa: E501
        """
        pass

    def test_update_occurrence(self):
        """Test case for update_occurrence

        Updates an existing `Occurrence`.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
