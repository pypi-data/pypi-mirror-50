# coding: utf-8

import pprint
import re  # noqa: F401

import six


class DocumentInfo(object):

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    swagger_types = {
        "count": "int",
        "ids": "list[str]",
        "total_size_estimate": "str",
    }

    attribute_map = {
        "count": "count",
        "ids": "ids",
        "total_size_estimate": "totalSizeEstimate",
    }

    def __init__(
        self, count=None, ids=None, total_size_estimate=None
    ):  # noqa: E501
        """DocumentInfo - meta data relating to the documents in a single filing"""  # noqa: E501

        self._count = None
        self._ids = None
        self._total_size_estimate = None
        self.discriminator = None

        self.count = count
        if ids is not None:
            self.ids = ids
        if total_size_estimate is not None:
            self.total_size_estimate = total_size_estimate

    @property
    def count(self):
        """Gets the count of this DocumentInfo.  # noqa: E501

        The number of documents belonging to this filing.  # noqa: E501

        :return: The count of this DocumentInfo.  # noqa: E501
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this DocumentInfo.

        The number of documents belonging to this filing.  # noqa: E501

        :param count: The count of this DocumentInfo.  # noqa: E501
        :type: int
        """
        if count is None:
            raise ValueError(
                "Invalid value for `count`, must not be `None`"
            )  # noqa: E501

        self._count = count

    @property
    def ids(self):
        """Gets the ids of this DocumentInfo.  # noqa: E501

        The set of the document ids for this filing.  # noqa: E501

        :return: The ids of this DocumentInfo.  # noqa: E501
        :rtype: list[str]
        """
        return self._ids

    @ids.setter
    def ids(self, ids):
        """Sets the ids of this DocumentInfo.

        The set of the document ids for the returned filing.  # noqa: E501

        :param ids: The ids of this DocumentInfo.  # noqa: E501
        :type: list[str]
        """

        self._ids = ids

    @property
    def total_size_estimate(self):
        """Gets the total_size_estimate of this DocumentInfo.  # noqa: E501

        The sum of size estimations of the all the documents belonging to this filing.  # noqa: E501

        :return: The total_size_estimate of this DocumentInfo.  # noqa: E501
        :rtype: str
        """
        return self._total_size_estimate

    @total_size_estimate.setter
    def total_size_estimate(self, total_size_estimate):
        """Sets the total_size_estimate of this DocumentInfo.

        The sum of size estimations of the all the documents belonging to this filing.  # noqa: E501

        :param total_size_estimate: The total_size_estimate of this DocumentInfo.  # noqa: E501
        :type: str
        """

        self._total_size_estimate = total_size_estimate

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
        # if issubclass(DocumentInfo, dict):
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
        if not isinstance(other, DocumentInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
