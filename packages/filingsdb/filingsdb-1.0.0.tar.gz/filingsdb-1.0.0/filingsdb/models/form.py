# coding: utf-8

import pprint
import re  # noqa: F401

import six


class Form(object):

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    swagger_types = {"description": "str", "form_type": "str"}

    attribute_map = {"description": "description", "form_type": "formType"}

    def __init__(self, description=None, form_type=None):  # noqa: E501
        """Form - an instance of a single form type containing its description"""  # noqa: E501

        self._description = None
        self._form_type = None
        self.discriminator = None

        self.description = description
        self.form_type = form_type

    @property
    def description(self):
        """Gets the description of this Form.  # noqa: E501

        The description of a form type.  # noqa: E501

        :return: The description of this Form.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Form.

        The description of a form type.  # noqa: E501

        :param description: The description of this Form.  # noqa: E501
        :type: str
        """
        if description is None:
            raise ValueError(
                "Invalid value for `description`, must not be `None`"
            )  # noqa: E501

        self._description = description

    @property
    def form_type(self):
        """Gets the form_type of this Form.  # noqa: E501

        The form type in the form of a short code.  # noqa: E501

        :return: The form_type of this Form.  # noqa: E501
        :rtype: str
        """
        return self._form_type

    @form_type.setter
    def form_type(self, form_type):
        """Sets the form_type of this Form.

        The form type in the form of a short code.  # noqa: E501

        :param form_type: The form_type of this Form.  # noqa: E501
        :type: str
        """
        if form_type is None:
            raise ValueError(
                "Invalid value for `form_type`, must not be `None`"
            )  # noqa: E501

        self._form_type = form_type

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
        # if issubclass(Form, dict):
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
        if not isinstance(other, Form):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
