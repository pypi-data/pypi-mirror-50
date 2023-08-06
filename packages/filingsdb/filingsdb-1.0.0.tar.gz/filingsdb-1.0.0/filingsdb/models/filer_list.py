# coding: utf-8

import pprint
import re  # noqa: F401

import six

from filingsdb.models.filer import Filer  # noqa: F401,E501


class FilerList(object):

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    swagger_types = {"items": "list[Filer]", "size": "int"}

    attribute_map = {"items": "items", "size": "size"}

    def __init__(self, items=None, size=None):  # noqa: E501
        """FilerList - a list of filer models"""  # noqa: E501

        self._items = None
        self._size = None
        self.discriminator = None

        self.items = items
        self.size = size

    @property
    def items(self):
        """Gets the items of this FilerList.  # noqa: E501

        The set of filers that matched the search term.  # noqa: E501

        :return: The items of this FilerList.  # noqa: E501
        :rtype: list[Filer]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this FilerList.

        The set of filers that matched the search term.  # noqa: E501

        :param items: The items of this FilerList.  # noqa: E501
        :type: list[Filer]
        """
        if items is None:
            raise ValueError(
                "Invalid value for `items`, must not be `None`"
            )  # noqa: E501

        self._items = items

    @property
    def size(self):
        """Gets the size of this FilerList.  # noqa: E501

        The amount of filers that were returned in the current request.  # noqa: E501

        :return: The size of this FilerList.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this FilerList.

        The amount of filers that were returned in the current request.  # noqa: E501

        :param size: The size of this FilerList.  # noqa: E501
        :type: int
        """
        if size is None:
            raise ValueError(
                "Invalid value for `size`, must not be `None`"
            )  # noqa: E501

        self._size = size

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
        # if issubclass(FilerList, dict):
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
        if not isinstance(other, FilerList):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
