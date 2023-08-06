# coding: utf-8

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from filingsdb.api_client import ApiClient


class FilingApi(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_filing(self, id, **kwargs):  # noqa: E501
        """Get A Single Filing  # noqa: E501

        Returns the single filing that matches the provided accession id.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_filing(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: The accession id of the filing to retrieve. (required)
        :return: FilingResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.get_filing_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_filing_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_filing_with_http_info(self, id, **kwargs):  # noqa: E501
        """Get A Single Filing  # noqa: E501

        Returns the single filing that matches the provided accession id.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_filing_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: The accession id of the filing to retrieve. (required)
        :return: FilingResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ["id"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        params = locals()
        for key, val in six.iteritems(params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_filing" % key
                )
            params[key] = val
        del params["kwargs"]
        # verify the required parameter 'id' is set
        if "id" not in params or params["id"] is None:
            raise ValueError(
                "Missing the required parameter `id` when calling `get_filing`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "id" in params:
            path_params["id"] = params["id"]  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            "/filings/accession/{id}",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="FilingResponse",  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get("async_req"),
            _return_http_data_only=params.get("_return_http_data_only"),
            _preload_content=params.get("_preload_content", True),
            _request_timeout=params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def list_all_filings(self, **kwargs):  # noqa: E501
        """List All  # noqa: E501

        Returns sets of all filings in order  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_all_filings(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str end: The right boundary on a chronological range of filings. The default is the current time.
        :param str form_type: The form type restriction that any returned filings must match.
        :param int page: The page index of the set of filings to return. Default is 1.
        :param int size: The length of the set of filings to return. Ranges from 10-50 and the default is 10.
        :param int sort: The chronological sort order of the filings that were returned in the current request. A value of 1 indicates descending order and -1 indicates ascending order. The default is 1.
        :param str start: The left boundary on a chronological range of filings. The default is 1970-01-01.
        :return: FilingsListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.list_all_filings_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.list_all_filings_with_http_info(
                **kwargs
            )  # noqa: E501
            return data

    def list_all_filings_with_http_info(self, **kwargs):  # noqa: E501
        """List All  # noqa: E501

        Returns sets of all filings in order  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_all_filings_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str end: The right boundary on a chronological range of filings. The default is the current time.
        :param str form_type: The form type restriction that any returned filings must match.
        :param int page: The page index of the set of filings to return. Default is 1.
        :param int size: The length of the set of filings to return. Ranges from 10-50 and the default is 10.
        :param int sort: The chronological sort order of the filings that were returned in the current request. A value of 1 indicates descending order and -1 indicates ascending order. The default is 1.
        :param str start: The left boundary on a chronological range of filings. The default is 1970-01-01.
        :return: FilingsListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = [
            "end",
            "form_type",
            "page",
            "size",
            "sort",
            "start",
        ]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        params = locals()
        for key, val in six.iteritems(params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_all_filings" % key
                )
            params[key] = val
        del params["kwargs"]

        collection_formats = {}

        path_params = {}

        query_params = []
        if "end" in params:
            query_params.append(("end", params["end"]))  # noqa: E501
        if "form_type" in params:
            query_params.append(
                ("formType", params["form_type"])
            )  # noqa: E501
        if "page" in params:
            query_params.append(("page", params["page"]))  # noqa: E501
        if "size" in params:
            query_params.append(("size", params["size"]))  # noqa: E501
        if "sort" in params:
            query_params.append(("sort", params["sort"]))  # noqa: E501
        if "start" in params:
            query_params.append(("start", params["start"]))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            "/filings/all",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="FilingsListResponse",  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get("async_req"),
            _return_http_data_only=params.get("_return_http_data_only"),
            _preload_content=params.get("_preload_content", True),
            _request_timeout=params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def list_filings_by_cik(self, **kwargs):  # noqa: E501
        """List By Central Index Key  # noqa: E501

        Returns a set of filings that match a filer CIK (Central Index Key).  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_filings_by_cik(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str end: The right boundary on a chronological range of filings. The default is the current time.
        :param str form_type: The form type restriction that any returned filings must match.
        :param int page: The page index of the set of filings to return. Default is 1.
        :param int size: The length of the set of filings to return. Ranges from 10-50 and the default is 10.
        :param int sort: The chronological sort order of the filings that were returned in the current request. A value of 1 indicates descending order and -1 indicates ascending order. The default is 1.
        :param str start: The left boundary on a chronological range of filings. The default is 1970-01-01.
        :param str query: The filter term.
        :return: FilingsListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.list_filings_by_cik_with_http_info(
                **kwargs
            )  # noqa: E501
        else:
            (data) = self.list_filings_by_cik_with_http_info(
                **kwargs
            )  # noqa: E501
            return data

    def list_filings_by_cik_with_http_info(self, **kwargs):  # noqa: E501
        """List By Central Index Key  # noqa: E501

        Returns a set of filings that match a filer CIK (Central Index Key).  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_filings_by_cik_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str end: The right boundary on a chronological range of filings. The default is the current time.
        :param str form_type: The form type restriction that any returned filings must match.
        :param int page: The page index of the set of filings to return. Default is 1.
        :param int size: The length of the set of filings to return. Ranges from 10-50 and the default is 10.
        :param int sort: The chronological sort order of the filings that were returned in the current request. A value of 1 indicates descending order and -1 indicates ascending order. The default is 1.
        :param str start: The left boundary on a chronological range of filings. The default is 1970-01-01.
        :param str query: The filter term.
        :return: FilingsListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = [
            "end",
            "form_type",
            "page",
            "size",
            "sort",
            "start",
            "query",
        ]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        params = locals()
        for key, val in six.iteritems(params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_filings_by_cik" % key
                )
            params[key] = val
        del params["kwargs"]

        collection_formats = {}

        path_params = {}

        query_params = []
        if "end" in params:
            query_params.append(("end", params["end"]))  # noqa: E501
        if "form_type" in params:
            query_params.append(
                ("formType", params["form_type"])
            )  # noqa: E501
        if "page" in params:
            query_params.append(("page", params["page"]))  # noqa: E501
        if "size" in params:
            query_params.append(("size", params["size"]))  # noqa: E501
        if "sort" in params:
            query_params.append(("sort", params["sort"]))  # noqa: E501
        if "start" in params:
            query_params.append(("start", params["start"]))  # noqa: E501
        if "query" in params:
            query_params.append(("query", params["query"]))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            "/filings/cik",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="FilingsListResponse",  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get("async_req"),
            _return_http_data_only=params.get("_return_http_data_only"),
            _preload_content=params.get("_preload_content", True),
            _request_timeout=params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def list_filings_by_filer(self, **kwargs):  # noqa: E501
        """List By Filer Name  # noqa: E501

        Returns a set of filings that match a filer name  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_filings_by_filer(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str end: The right boundary on a chronological range of filings. The default is the current time.
        :param str form_type: The form type restriction that any returned filings must match.
        :param int page: The page index of the set of filings to return. Default is 1.
        :param int size: The length of the set of filings to return. Ranges from 10-50 and the default is 10.
        :param int sort: The chronological sort order of the filings that were returned in the current request. A value of 1 indicates descending order and -1 indicates ascending order. The default is 1.
        :param str start: The left boundary on a chronological range of filings. The default is 1970-01-01.
        :param str query: The filter term.
        :return: FilingsListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.list_filings_by_filer_with_http_info(
                **kwargs
            )  # noqa: E501
        else:
            (data) = self.list_filings_by_filer_with_http_info(
                **kwargs
            )  # noqa: E501
            return data

    def list_filings_by_filer_with_http_info(self, **kwargs):  # noqa: E501
        """List By Filer Name  # noqa: E501

        Returns a set of filings that match a filer name  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_filings_by_filer_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str end: The right boundary on a chronological range of filings. The default is the current time.
        :param str form_type: The form type restriction that any returned filings must match.
        :param int page: The page index of the set of filings to return. Default is 1.
        :param int size: The length of the set of filings to return. Ranges from 10-50 and the default is 10.
        :param int sort: The chronological sort order of the filings that were returned in the current request. A value of 1 indicates descending order and -1 indicates ascending order. The default is 1.
        :param str start: The left boundary on a chronological range of filings. The default is 1970-01-01.
        :param str query: The filter term.
        :return: FilingsListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = [
            "end",
            "form_type",
            "page",
            "size",
            "sort",
            "start",
            "query",
        ]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        params = locals()
        for key, val in six.iteritems(params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_filings_by_filer" % key
                )
            params[key] = val
        del params["kwargs"]

        collection_formats = {}

        path_params = {}

        query_params = []
        if "end" in params:
            query_params.append(("end", params["end"]))  # noqa: E501
        if "form_type" in params:
            query_params.append(
                ("formType", params["form_type"])
            )  # noqa: E501
        if "page" in params:
            query_params.append(("page", params["page"]))  # noqa: E501
        if "size" in params:
            query_params.append(("size", params["size"]))  # noqa: E501
        if "sort" in params:
            query_params.append(("sort", params["sort"]))  # noqa: E501
        if "start" in params:
            query_params.append(("start", params["start"]))  # noqa: E501
        if "query" in params:
            query_params.append(("query", params["query"]))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            "/filings/filer",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="FilingsListResponse",  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get("async_req"),
            _return_http_data_only=params.get("_return_http_data_only"),
            _preload_content=params.get("_preload_content", True),
            _request_timeout=params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def list_filings_by_symbol(self, **kwargs):  # noqa: E501
        """List By Symbol  # noqa: E501

        Returns a set of filings that match a symbol.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_filings_by_symbol(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str end: The right boundary on a chronological range of filings. The default is the current time.
        :param str form_type: The form type restriction that any returned filings must match.
        :param int page: The page index of the set of filings to return. Default is 1.
        :param int size: The length of the set of filings to return. Ranges from 10-50 and the default is 10.
        :param int sort: The chronological sort order of the filings that were returned in the current request. A value of 1 indicates descending order and -1 indicates ascending order. The default is 1.
        :param str start: The left boundary on a chronological range of filings. The default is 1970-01-01.
        :param str query: The filter term.
        :return: FilingsListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.list_filings_by_symbol_with_http_info(
                **kwargs
            )  # noqa: E501
        else:
            (data) = self.list_filings_by_symbol_with_http_info(
                **kwargs
            )  # noqa: E501
            return data

    def list_filings_by_symbol_with_http_info(self, **kwargs):  # noqa: E501
        """List By Symbol  # noqa: E501

        Returns a set of filings that match a symbol.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_filings_by_symbol_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str end: The right boundary on a chronological range of filings. The default is the current time.
        :param str form_type: The form type restriction that any returned filings must match.
        :param int page: The page index of the set of filings to return. Default is 1.
        :param int size: The length of the set of filings to return. Ranges from 10-50 and the default is 10.
        :param int sort: The chronological sort order of the filings that were returned in the current request. A value of 1 indicates descending order and -1 indicates ascending order. The default is 1.
        :param str start: The left boundary on a chronological range of filings. The default is 1970-01-01.
        :param str query: The filter term.
        :return: FilingsListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = [
            "end",
            "form_type",
            "page",
            "size",
            "sort",
            "start",
            "query",
        ]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        params = locals()
        for key, val in six.iteritems(params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_filings_by_symbol" % key
                )
            params[key] = val
        del params["kwargs"]

        collection_formats = {}

        path_params = {}

        query_params = []
        if "end" in params:
            query_params.append(("end", params["end"]))  # noqa: E501
        if "form_type" in params:
            query_params.append(
                ("formType", params["form_type"])
            )  # noqa: E501
        if "page" in params:
            query_params.append(("page", params["page"]))  # noqa: E501
        if "size" in params:
            query_params.append(("size", params["size"]))  # noqa: E501
        if "sort" in params:
            query_params.append(("sort", params["sort"]))  # noqa: E501
        if "start" in params:
            query_params.append(("start", params["start"]))  # noqa: E501
        if "query" in params:
            query_params.append(("query", params["query"]))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            "/filings/symbol",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="FilingsListResponse",  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get("async_req"),
            _return_http_data_only=params.get("_return_http_data_only"),
            _preload_content=params.get("_preload_content", True),
            _request_timeout=params.get("_request_timeout"),
            collection_formats=collection_formats,
        )
