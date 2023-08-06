# coding: utf-8

import pprint
import re  # noqa: F401

import six

from filingsdb.models.filing import Filing  # noqa: F401,E501


class FilingsList(object):

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    swagger_types = {
        "has_next_page": "bool",
        "has_previous_page": "bool",
        "items": "list[Filing]",
        "page": "int",
        "size": "int",
        "sort": "str",
        "total_count": "int",
        "total_pages": "int",
    }

    attribute_map = {
        "has_next_page": "hasNextPage",
        "has_previous_page": "hasPreviousPage",
        "items": "items",
        "page": "page",
        "size": "size",
        "sort": "sort",
        "total_count": "totalCount",
        "total_pages": "totalPages",
    }

    def __init__(
        self,
        has_next_page=None,
        has_previous_page=None,
        items=None,
        page=None,
        size=None,
        sort=None,
        total_count=None,
        total_pages=None,
    ):  # noqa: E501
        """FilingsList - a list of filings"""  # noqa: E501

        self._has_next_page = None
        self._has_previous_page = None
        self._items = None
        self._page = None
        self._size = None
        self._sort = None
        self._total_count = None
        self._total_pages = None
        self.discriminator = None

        self.has_next_page = has_next_page
        self.has_previous_page = has_previous_page
        self.items = items
        self.page = page
        self.size = size
        self.sort = sort
        self.total_count = total_count
        self.total_pages = total_pages

    @property
    def has_next_page(self):
        """Gets the has_next_page of this FilingsList.  # noqa: E501

        Whether or not a request with the same parameters has a next page of filings available.  # noqa: E501

        :return: The has_next_page of this FilingsList.  # noqa: E501
        :rtype: bool
        """
        return self._has_next_page

    @has_next_page.setter
    def has_next_page(self, has_next_page):
        """Sets the has_next_page of this FilingsList.

        Whether or not a request with the same parameters has a next page of filings available.  # noqa: E501

        :param has_next_page: The has_next_page of this FilingsList.  # noqa: E501
        :type: bool
        """
        if has_next_page is None:
            raise ValueError(
                "Invalid value for `has_next_page`, must not be `None`"
            )  # noqa: E501

        self._has_next_page = has_next_page

    @property
    def has_previous_page(self):
        """Gets the has_previous_page of this FilingsList.  # noqa: E501

        Whether or not a request with the same parameters has a previous page of filings available.  # noqa: E501

        :return: The has_previous_page of this FilingsList.  # noqa: E501
        :rtype: bool
        """
        return self._has_previous_page

    @has_previous_page.setter
    def has_previous_page(self, has_previous_page):
        """Sets the has_previous_page of this FilingsList.

        Whether or not a request with the same parameters has a previous page of filings available.  # noqa: E501

        :param has_previous_page: The has_previous_page of this FilingsList.  # noqa: E501
        :type: bool
        """
        if has_previous_page is None:
            raise ValueError(
                "Invalid value for `has_previous_page`, must not be `None`"
            )  # noqa: E501

        self._has_previous_page = has_previous_page

    @property
    def items(self):
        """Gets the items of this FilingsList.  # noqa: E501

        The set of filings that were returned in the current request.  # noqa: E501

        :return: The items of this FilingsList.  # noqa: E501
        :rtype: list[Filing]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this FilingsList.

        The set of filings that were returned in the current request.  # noqa: E501

        :param items: The items of this FilingsList.  # noqa: E501
        :type: list[Filing]
        """
        if items is None:
            raise ValueError(
                "Invalid value for `items`, must not be `None`"
            )  # noqa: E501

        self._items = items

    @property
    def page(self):
        """Gets the page of this FilingsList.  # noqa: E501

        The page index of the set of filings returned in the response.  # noqa: E501

        :return: The page of this FilingsList.  # noqa: E501
        :rtype: int
        """
        return self._page

    @page.setter
    def page(self, page):
        """Sets the page of this FilingsList.

        The page index of the set of filings returned in the response.  # noqa: E501

        :param page: The page of this FilingsList.  # noqa: E501
        :type: int
        """
        if page is None:
            raise ValueError(
                "Invalid value for `page`, must not be `None`"
            )  # noqa: E501

        self._page = page

    @property
    def size(self):
        """Gets the size of this FilingsList.  # noqa: E501

        The length of the set of filings returned in the response.  # noqa: E501

        :return: The size of this FilingsList.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this FilingsList.

        The length of the set of filings returned in the response.  # noqa: E501

        :param size: The size of this FilingsList.  # noqa: E501
        :type: int
        """
        if size is None:
            raise ValueError(
                "Invalid value for `size`, must not be `None`"
            )  # noqa: E501

        self._size = size

    @property
    def sort(self):
        """Gets the sort of this FilingsList.  # noqa: E501

        The chronological sort order of the filings that were returned in the current request.  # noqa: E501

        :return: The sort of this FilingsList.  # noqa: E501
        :rtype: str
        """
        return self._sort

    @sort.setter
    def sort(self, sort):
        """Sets the sort of this FilingsList.

        The chronological sort order of the filings that were returned in the current request.  # noqa: E501

        :param sort: The sort of this FilingsList.  # noqa: E501
        :type: str
        """
        if sort is None:
            raise ValueError(
                "Invalid value for `sort`, must not be `None`"
            )  # noqa: E501

        self._sort = sort

    @property
    def total_count(self):
        """Gets the total_count of this FilingsList.  # noqa: E501

        The total amount of filings that match the current request parameters.  # noqa: E501

        :return: The total_count of this FilingsList.  # noqa: E501
        :rtype: int
        """
        return self._total_count

    @total_count.setter
    def total_count(self, total_count):
        """Sets the total_count of this FilingsList.

        The total amount of filings that match the current request parameters.  # noqa: E501

        :param total_count: The total_count of this FilingsList.  # noqa: E501
        :type: int
        """
        if total_count is None:
            raise ValueError(
                "Invalid value for `total_count`, must not be `None`"
            )  # noqa: E501

        self._total_count = total_count

    @property
    def total_pages(self):
        """Gets the total_pages of this FilingsList.  # noqa: E501

        The total amount of pages of filings that match the current request parameters.  # noqa: E501

        :return: The total_pages of this FilingsList.  # noqa: E501
        :rtype: int
        """
        return self._total_pages

    @total_pages.setter
    def total_pages(self, total_pages):
        """Sets the total_pages of this FilingsList.

        The total amount of pages of filings that match the current request parameters.  # noqa: E501

        :param total_pages: The total_pages of this FilingsList.  # noqa: E501
        :type: int
        """
        if total_pages is None:
            raise ValueError(
                "Invalid value for `total_pages`, must not be `None`"
            )  # noqa: E501

        self._total_pages = total_pages

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(
                        lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                        value,
                    )
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        # if issubclass(FilingsList, dict):
        #     for key, value in self.items():
        #         result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, FilingsList):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
