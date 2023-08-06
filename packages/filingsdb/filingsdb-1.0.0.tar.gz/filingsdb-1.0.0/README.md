# FilingsDB Python Library

[![Build Status](https://travis-ci.org/filingsdb/filingsdb-python.svg?branch=master)](https://travis-ci.org/filingsdb/filingsdb-python)
[![Coverage Status](https://coveralls.io/repos/github/filingsdb/filingsdb-python/badge.svg?branch=master)](https://coveralls.io/github/filingsdb/filingsdb-python?branch=master)

The python client library for the [FilingsDB API](https://filingsdb.com/api/docs/)

The FilingsDB API is a comprehensive rest-based service that returns the full text of corporate filings submitted to the SEC EDGAR site by publicly traded firms.

## Features

- Retrieve the full text of corporate filings as soon as they are submitted
- Historical filings of the top 5000 U.S corporations back to ~ year 1999
- Support for a broad set of form types (10-Q, 8-K, 4, 10-K, S-1 etc.)
- Search & sort filings by CIK, traded symbol, company name, form type, date
- Search & sort corporations by name, symbol, CIK, SIC code
- Text search coming soon!

## Requirements

Python 2.7 and 3.4+

## Installation

### pip install

You can install directly from Github

```sh
pip install https://github.com/filingsdb/filingsdb-python/zipball/master
```

Then import the package:

```python
import filingsdb
```

### From source

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```

## Usage

After following the [installation procedure](#installation), you can begin to make requests and interact with the api. If you need an api key or a demo, please follow the instructions on the [site](https://filingsdb.com/api/).

### Filings

The following code example will return a set of the most recent corporate filings for Slack -

```python
import filingsdb
from filingsdb.rest import ApiException
from pprint import pprint

conf = filingsdb.Configuration()
conf.api_key = "YOUR_KEY_HERE"
filings = filingsdb.FilingApi(filingsdb.ApiClient(conf))

try:
    # request the 10 most recent Slack Technologies Inc (NYSE: WORK) filings
    resp = filings.list_filings_by_filer(query="slack")
    pprint(resp)
except ApiException as e:
    print("Encountered an exception: %s\n" % e)

```

### More

There a lot more ways to request filings, form types, and filer entities - please see the [site docs](https://filingsdb.com/api/) or the python model docs here for more information on API usage.


## Documentation for API Endpoints

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*DocumentApi* | [**get_document**](docs/DocumentApi.md#get_document) | **GET** /documents/id/{id} | Get A Single Document
*FilerApi* | [**search_filers**](docs/FilerApi.md#search_filers) | **GET** /filers/search | Search Filers
*FilingApi* | [**get_filing**](docs/FilingApi.md#get_filing) | **GET** /filings/accession/{id} | Get A Single Filing
*FilingApi* | [**list_all_filings**](docs/FilingApi.md#list_all_filings) | **GET** /filings/all | List All
*FilingApi* | [**list_filings_by_cik**](docs/FilingApi.md#list_filings_by_cik) | **GET** /filings/cik | List By Central Index Key
*FilingApi* | [**list_filings_by_filer**](docs/FilingApi.md#list_filings_by_filer) | **GET** /filings/filer | List By Filer Name
*FilingApi* | [**list_filings_by_symbol**](docs/FilingApi.md#list_filings_by_symbol) | **GET** /filings/symbol | List By Symbol
*FormApi* | [**list_forms**](docs/FormApi.md#list_forms) | **GET** /forms/list | List Available Forms


## Documentation For Models

- [Document](docs/Document.md)
- [DocumentInfo](docs/DocumentInfo.md)
- [DocumentResponse](docs/DocumentResponse.md)
- [ErrorResponse](docs/ErrorResponse.md)
- [Filer](docs/Filer.md)
- [FilerList](docs/FilerList.md)
- [FilerListResponse](docs/FilerListResponse.md)
- [Filing](docs/Filing.md)
- [FilingResponse](docs/FilingResponse.md)
- [FilingsList](docs/FilingsList.md)
- [FilingsListResponse](docs/FilingsListResponse.md)
- [Form](docs/Form.md)
- [FormList](docs/FormList.md)
- [FormListResponse](docs/FormListResponse.md)
- [UnauthorizedResponse](docs/UnauthorizedResponse.md)
