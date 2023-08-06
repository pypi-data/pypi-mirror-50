# coding: utf-8

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from filingsdb.api_client import ApiClient


class FilerApi(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def search_filers(self, query, **kwargs):  # noqa: E501
        """Search Filers  # noqa: E501

        Returns a set of filer entities that match the query term.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.search_filers(query, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str query: The search term to match filers on. Can be a symbol, name, or cik. (required)
        :return: FilerListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.search_filers_with_http_info(
                query, **kwargs
            )  # noqa: E501
        else:
            (data) = self.search_filers_with_http_info(
                query, **kwargs
            )  # noqa: E501
            return data

    def search_filers_with_http_info(self, query, **kwargs):  # noqa: E501
        """Search Filers  # noqa: E501

        Returns a set of filer entities that match the query term.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.search_filers_with_http_info(query, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str query: The search term to match filers on. Can be a symbol, name, or cik. (required)
        :return: FilerListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ["query"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        params = locals()
        for key, val in six.iteritems(params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method search_filers" % key
                )
            params[key] = val
        del params["kwargs"]
        # verify the required parameter 'query' is set
        if "query" not in params or params["query"] is None:
            raise ValueError(
                "Missing the required parameter `query` when calling `search_filers`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if "query" in params:
            query_params.append(("query", params["query"]))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            "/filers/search",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="FilerListResponse",  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get("async_req"),
            _return_http_data_only=params.get("_return_http_data_only"),
            _preload_content=params.get("_preload_content", True),
            _request_timeout=params.get("_request_timeout"),
            collection_formats=collection_formats,
        )
