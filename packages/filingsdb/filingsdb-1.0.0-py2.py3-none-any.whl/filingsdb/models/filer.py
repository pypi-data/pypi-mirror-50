# coding: utf-8

import pprint
import re  # noqa: F401

import six


class Filer(object):

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    swagger_types = {
        "cik": "str",
        "name": "str",
        "sic": "str",
        "sic_desc": "str",
        "symbol": "str",
    }

    attribute_map = {
        "cik": "cik",
        "name": "name",
        "sic": "sic",
        "sic_desc": "sic_desc",
        "symbol": "symbol",
    }

    def __init__(
        self, cik=None, name=None, sic=None, sic_desc=None, symbol=None
    ):  # noqa: E501
        """Filer - a filer, a corporate entity that submits filings"""  # noqa: E501

        self._cik = None
        self._name = None
        self._sic = None
        self._sic_desc = None
        self._symbol = None
        self.discriminator = None

        self.cik = cik
        self.name = name
        if sic is not None:
            self.sic = sic
        if sic_desc is not None:
            self.sic_desc = sic_desc
        self.symbol = symbol

    @property
    def cik(self):
        """Gets the cik of this Filer.  # noqa: E501

        The CIK (Central Index Key) of the filing entity.  # noqa: E501

        :return: The cik of this Filer.  # noqa: E501
        :rtype: str
        """
        return self._cik

    @cik.setter
    def cik(self, cik):
        """Sets the cik of this Filer.

        The CIK (Central Index Key) of the filing entity.  # noqa: E501

        :param cik: The cik of this Filer.  # noqa: E501
        :type: str
        """
        if cik is None:
            raise ValueError(
                "Invalid value for `cik`, must not be `None`"
            )  # noqa: E501

        self._cik = cik

    @property
    def name(self):
        """Gets the name of this Filer.  # noqa: E501

        The name of the filing entity.  # noqa: E501

        :return: The name of this Filer.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Filer.

        The name of the filing entity.  # noqa: E501

        :param name: The name of this Filer.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError(
                "Invalid value for `name`, must not be `None`"
            )  # noqa: E501

        self._name = name

    @property
    def sic(self):
        """Gets the sic of this Filer.  # noqa: E501

        An optional SIC (Standard Industry Classification) code of a filer.  # noqa: E501

        :return: The sic of this Filer.  # noqa: E501
        :rtype: str
        """
        return self._sic

    @sic.setter
    def sic(self, sic):
        """Sets the sic of this Filer.

        An optional SIC (Standard Industry Classification) code of a filer.  # noqa: E501

        :param sic: The sic of this Filer.  # noqa: E501
        :type: str
        """

        self._sic = sic

    @property
    def sic_desc(self):
        """Gets the sic_desc of this Filer.  # noqa: E501

        An optional description of the SIC code of a filer.  # noqa: E501

        :return: The sic_desc of this Filer.  # noqa: E501
        :rtype: str
        """
        return self._sic_desc

    @sic_desc.setter
    def sic_desc(self, sic_desc):
        """Sets the sic_desc of this Filer.

        An optional description of the SIC code of a filer.  # noqa: E501

        :param sic_desc: The sic_desc of this Filer.  # noqa: E501
        :type: str
        """

        self._sic_desc = sic_desc

    @property
    def symbol(self):
        """Gets the symbol of this Filer.  # noqa: E501

        The symbol of the filing entity.  # noqa: E501

        :return: The symbol of this Filer.  # noqa: E501
        :rtype: str
        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        """Sets the symbol of this Filer.

        The symbol of the filing entity.  # noqa: E501

        :param symbol: The symbol of this Filer.  # noqa: E501
        :type: str
        """
        if symbol is None:
            raise ValueError(
                "Invalid value for `symbol`, must not be `None`"
            )  # noqa: E501

        self._symbol = symbol

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
        # if issubclass(Filer, dict):
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
        if not isinstance(other, Filer):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
