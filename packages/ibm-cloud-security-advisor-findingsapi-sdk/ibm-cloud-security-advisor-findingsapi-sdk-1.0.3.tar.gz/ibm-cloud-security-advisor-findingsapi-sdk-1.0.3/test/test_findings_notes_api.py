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
from api.findings_notes_api import FindingsNotesApi  # noqa: E501
from ibm_security_advisor_findings_api_client.rest import ApiException


class TestFindingsNotesApi(unittest.TestCase):
    """FindingsNotesApi unit test stubs"""

    def setUp(self):
        self.api = api.findings_notes_api.FindingsNotesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_note(self):
        """Test case for create_note

        Creates a new `Note`.  # noqa: E501
        """
        pass

    def test_delete_note(self):
        """Test case for delete_note

        Deletes the given `Note` from the system.  # noqa: E501
        """
        pass

    def test_get_note(self):
        """Test case for get_note

        Returns the requested `Note`.  # noqa: E501
        """
        pass

    def test_get_occurrence_note(self):
        """Test case for get_occurrence_note

        Gets the `Note` attached to the given `Occurrence`.  # noqa: E501
        """
        pass

    def test_list_notes(self):
        """Test case for list_notes

        Lists all `Notes` for a given provider.  # noqa: E501
        """
        pass

    def test_update_note(self):
        """Test case for update_note

        Updates an existing `Note`.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
