# coding: utf-8

import pprint
import re  # noqa: F401

import six

from filingsdb.models.form import Form  # noqa: F401,E501


class FormList(object):

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    swagger_types = {"items": "list[Form]", "size": "int"}

    attribute_map = {"items": "items", "size": "size"}

    def __init__(self, items=None, size=None):  # noqa: E501
        """FormList - a list of form models"""  # noqa: E501

        self._items = None
        self._size = None
        self.discriminator = None

        self.items = items
        self.size = size

    @property
    def items(self):
        """Gets the items of this FormList.  # noqa: E501

        The set of forms.  # noqa: E501

        :return: The items of this FormList.  # noqa: E501
        :rtype: list[Form]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this FormList.

        The set of forms.  # noqa: E501

        :param items: The items of this FormList.  # noqa: E501
        :type: list[Form]
        """
        if items is None:
            raise ValueError(
                "Invalid value for `items`, must not be `None`"
            )  # noqa: E501

        self._items = items

    @property
    def size(self):
        """Gets the size of this FormList.  # noqa: E501

        The amount of form types that were returned in the current request.  # noqa: E501

        :return: The size of this FormList.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this FormList.

        The amount of form types that were returned in the current request.  # noqa: E501

        :param size: The size of this FormList.  # noqa: E501
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
        # if issubclass(FormList, dict):
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
        if not isinstance(other, FormList):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
