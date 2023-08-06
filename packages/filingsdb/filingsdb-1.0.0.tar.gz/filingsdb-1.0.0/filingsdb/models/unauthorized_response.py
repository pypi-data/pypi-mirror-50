# coding: utf-8

import pprint
import re  # noqa: F401

import six


class UnauthorizedResponse(object):

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    swagger_types = {"message": "str"}

    attribute_map = {"message": "message"}

    def __init__(self, message=None):  # noqa: E501
        """UnauthorizedResponse - response that occurs when a request is unauthenticated"""  # noqa: E501

        self._message = None
        self.discriminator = None

        self.message = message

    @property
    def message(self):
        """Gets the message of this UnauthorizedResponse.  # noqa: E501

        A message explaining that the access token is missing or invalid  # noqa: E501

        :return: The message of this UnauthorizedResponse.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this UnauthorizedResponse.

        A message explaining that the access token is missing or invalid  # noqa: E501

        :param message: The message of this UnauthorizedResponse.  # noqa: E501
        :type: str
        """
        if message is None:
            raise ValueError(
                "Invalid value for `message`, must not be `None`"
            )  # noqa: E501

        self._message = message

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
        # if issubclass(UnauthorizedResponse, dict):
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
        if not isinstance(other, UnauthorizedResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
