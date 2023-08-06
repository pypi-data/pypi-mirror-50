IBM Cloud Security Advisor Findings API Python SDK 
==================

This repository contains the released Python client SDK for IBM Cloud ecurity Advisor Findings API . Check out our [API
documentation](https://cloud.ibm.com/apidocs/security-advisor/findings) for more details.

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

you can install latest version by

```sh
pip install ibm-cloud-security-advisor-findingsapi-sdk
```

Since the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python.git`)

Then import the package:
```python
import ibm_security_advisor_findings_api_client 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import ibm_security_advisor_findings_api_client
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
 
from __future__ import print_function
import time
import ibm_security_advisor_findings_api_client 
from ibm_security_advisor_findings_api_client.rest import ApiException
from pprint import pprint

note =     {
        "kind": "FINDING",
        "short_description": "Test Finding",
        "long_description": "Test Finding",
        "provider_id": "TEST",
        "id": "test-finding",
        "reported_by": {
            "id": "test-finding",
            "title": "Test findings"
        },
        "finding": {
            "severity": "LOW",
            "next_steps": [{
                "title": "Verify open issues in link "
            }]
        }
}


# Configure API key authorization: UserMin
configuration = ibm_security_advisor_findings_api_client.Configuration()
#Change this to point to London endpoint
configuration.host= "https://us-south.secadvisor.cloud.ibm.com/findings"

api_instance = ibm_security_advisor_findings_api_client.FindingsNotesApi(ibm_security_advisor_findings_api_client.ApiClient(configuration))
body = note # ApiNote | Body for Note creation

authorization = 'Bearer <<YOUR IAM TOKEN>>`
account_id = 'Your account ID' # str | Account ID
provider_id = 'TEST' # str | Part of `parent`. This field contains the provider_id for example: providers/{provider_id}


try:
    # Creates a new `Note`.
    api_response = api_instance.create_note(body, authorization, account_id, provider_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FindingsNotesApi->create_note: %s\n" % e)
```

## Documentation for API Endpoints

All URIs are relative to */findings*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*FindingsGraphApi* | [**post_graph**](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/FindingsGraphApi.md#post_graph) | **POST** /v1/{account_id}/graph | query findings
*FindingsNotesApi* | [**create_note**](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/FindingsNotesApi.md#create_note) | **POST** /v1/{account_id}/providers/{provider_id}/notes | Creates a new &#x60;Note&#x60;.
*FindingsNotesApi* | [**delete_note**](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/FindingsNotesApi.md#delete_note) | **DELETE** /v1/{account_id}/providers/{provider_id}/notes/{note_id} | Deletes the given &#x60;Note&#x60; from the system.
*FindingsNotesApi* | [**get_note**](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/FindingsNotesApi.md#get_note) | **GET** /v1/{account_id}/providers/{provider_id}/notes/{note_id} | Returns the requested &#x60;Note&#x60;.
*FindingsNotesApi* | [**get_occurrence_note**](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/FindingsNotesApi.md#get_occurrence_note) | **GET** /v1/{account_id}/providers/{provider_id}/occurrences/{occurrence_id}/note | Gets the &#x60;Note&#x60; attached to the given &#x60;Occurrence&#x60;.
*FindingsNotesApi* | [**list_notes**](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/FindingsNotesApi.md#list_notes) | **GET** /v1/{account_id}/providers/{provider_id}/notes | Lists all &#x60;Notes&#x60; for a given provider.
*FindingsNotesApi* | [**update_note**](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/FindingsNotesApi.md#update_note) | **PUT** /v1/{account_id}/providers/{provider_id}/notes/{note_id} | Updates an existing &#x60;Note&#x60;.
*FindingsOccurrencesApi* | [**create_occurrence**](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/FindingsOccurrencesApi.md#create_occurrence) | **POST** /v1/{account_id}/providers/{provider_id}/occurrences | Creates a new &#x60;Occurrence&#x60;. Use this method to create &#x60;Occurrences&#x60; for a resource.
*FindingsOccurrencesApi* | [**delete_occurrence**](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/FindingsOccurrencesApi.md#delete_occurrence) | **DELETE** /v1/{account_id}/providers/{provider_id}/occurrences/{occurrence_id} | Deletes the given &#x60;Occurrence&#x60; from the system.
*FindingsOccurrencesApi* | [**get_occurrence**](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/FindingsOccurrencesApi.md#get_occurrence) | **GET** /v1/{account_id}/providers/{provider_id}/occurrences/{occurrence_id} | Returns the requested &#x60;Occurrence&#x60;.
*FindingsOccurrencesApi* | [**list_note_occurrences**](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/FindingsOccurrencesApi.md#list_note_occurrences) | **GET** /v1/{account_id}/providers/{provider_id}/notes/{note_id}/occurrences | Lists &#x60;Occurrences&#x60; referencing the specified &#x60;Note&#x60;. Use this method to get all occurrences referencing your &#x60;Note&#x60; across all your customer providers.
*FindingsOccurrencesApi* | [**list_occurrences**](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/FindingsOccurrencesApi.md#list_occurrences) | **GET** /v1/{account_id}/providers/{provider_id}/occurrences | Lists active &#x60;Occurrences&#x60; for a given provider matching the filters.
*FindingsOccurrencesApi* | [**update_occurrence**](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/FindingsOccurrencesApi.md#update_occurrence) | **PUT** /v1/{account_id}/providers/{provider_id}/occurrences/{occurrence_id} | Updates an existing &#x60;Occurrence&#x60;.

## Documentation For Models

 - [ApiEmpty](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/ApiEmpty.md)
 - [ApiListNoteOccurrencesResponse](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/ApiListNoteOccurrencesResponse.md)
 - [ApiListNotesResponse](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/ApiListNotesResponse.md)
 - [ApiListOccurrencesResponse](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/ApiListOccurrencesResponse.md)
 - [ApiListProvidersResponse](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/ApiListProvidersResponse.md)
 - [ApiNote](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/ApiNote.md)
 - [ApiNoteKind](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/ApiNoteKind.md)
 - [ApiNoteRelatedUrl](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/ApiNoteRelatedUrl.md)
 - [ApiOccurrence](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/ApiOccurrence.md)
 - [ApiProvider](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/ApiProvider.md)
 - [BreakdownCardElement](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/BreakdownCardElement.md)
 - [Card](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/Card.md)
 - [CardElement](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/CardElement.md)
 - [Certainty](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/Certainty.md)
 - [Context](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/Context.md)
 - [DataTransferred](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/DataTransferred.md)
 - [Finding](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/Finding.md)
 - [FindingCountValueType](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/FindingCountValueType.md)
 - [FindingType](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/FindingType.md)
 - [Kpi](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/Kpi.md)
 - [KpiType](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/KpiType.md)
 - [KpiValueType](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/KpiValueType.md)
 - [NetworkConnection](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/NetworkConnection.md)
 - [NumericCardElement](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/NumericCardElement.md)
 - [RemediationStep](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/RemediationStep.md)
 - [Reporter](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/Reporter.md)
 - [Section](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/Section.md)
 - [Severity](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/Severity.md)
 - [SocketAddress](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/SocketAddress.md)
 - [TimeSeriesCardElement](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/TimeSeriesCardElement.md)
 - [ValueType](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/docs/ValueType.md)

## Documentation For Authorization

Use "Bearer " + IAM TOKEN in api calls. Refer [Getting Started](#getting-started)
