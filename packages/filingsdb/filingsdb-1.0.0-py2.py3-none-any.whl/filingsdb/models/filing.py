# coding: utf-8

import pprint
import re  # noqa: F401

import six

from filingsdb.models.document_info import DocumentInfo  # noqa: F401,E501


class Filing(object):

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    swagger_types = {
        "accession": "str",
        "all_ci_ks": "list[str]",
        "all_symbols": "list[str]",
        "documents": "DocumentInfo",
        "edgar_time": "datetime",
        "edgar_url": "str",
        "filer": "str",
        "filer_relation": "str",
        "form_type": "str",
        "id": "str",
        "primary_cik": "str",
        "primary_symbol": "str",
    }

    attribute_map = {
        "accession": "accession",
        "all_ci_ks": "allCIKs",
        "all_symbols": "allSymbols",
        "documents": "documents",
        "edgar_time": "edgarTime",
        "edgar_url": "edgarURL",
        "filer": "filer",
        "filer_relation": "filerRelation",
        "form_type": "formType",
        "id": "id",
        "primary_cik": "primaryCIK",
        "primary_symbol": "primarySymbol",
    }

    def __init__(
        self,
        accession=None,
        all_ci_ks=None,
        all_symbols=None,
        documents=None,
        edgar_time=None,
        edgar_url=None,
        filer=None,
        filer_relation=None,
        form_type=None,
        id=None,
        primary_cik=None,
        primary_symbol=None,
    ):  # noqa: E501
        """Filing - a single filing object"""  # noqa: E501

        self._accession = None
        self._all_ci_ks = None
        self._all_symbols = None
        self._documents = None
        self._edgar_time = None
        self._edgar_url = None
        self._filer = None
        self._filer_relation = None
        self._form_type = None
        self._id = None
        self._primary_cik = None
        self._primary_symbol = None
        self.discriminator = None

        self.accession = accession
        self.all_ci_ks = all_ci_ks
        if all_symbols is not None:
            self.all_symbols = all_symbols
        self.documents = documents
        self.edgar_time = edgar_time
        self.edgar_url = edgar_url
        self.filer = filer
        self.filer_relation = filer_relation
        self.form_type = form_type
        self.id = id
        self.primary_cik = primary_cik
        if primary_symbol is not None:
            self.primary_symbol = primary_symbol

    @property
    def accession(self):
        """Gets the accession of this Filing.  # noqa: E501

        The accession id of the returned filing, assigned by the EDGAR system.  # noqa: E501

        :return: The accession of this Filing.  # noqa: E501
        :rtype: str
        """
        return self._accession

    @accession.setter
    def accession(self, accession):
        """Sets the accession of this Filing.

        The accession id of the returned filing, assigned by the EDGAR system.  # noqa: E501

        :param accession: The accession of this Filing.  # noqa: E501
        :type: str
        """
        if accession is None:
            raise ValueError(
                "Invalid value for `accession`, must not be `None`"
            )  # noqa: E501

        self._accession = accession

    @property
    def all_ci_ks(self):
        """Gets the all_ci_ks of this Filing.  # noqa: E501

        The CIKs of all filing entities associated with the returned filing.  # noqa: E501

        :return: The all_ci_ks of this Filing.  # noqa: E501
        :rtype: list[str]
        """
        return self._all_ci_ks

    @all_ci_ks.setter
    def all_ci_ks(self, all_ci_ks):
        """Sets the all_ci_ks of this Filing.

        The CIKs of all filing entities associated with the returned filing.  # noqa: E501

        :param all_ci_ks: The all_ci_ks of this Filing.  # noqa: E501
        :type: list[str]
        """
        if all_ci_ks is None:
            raise ValueError(
                "Invalid value for `all_ci_ks`, must not be `None`"
            )  # noqa: E501

        self._all_ci_ks = all_ci_ks

    @property
    def all_symbols(self):
        """Gets the all_symbols of this Filing.  # noqa: E501

        The stock exchange symbols of all filing entities associated with the returned filing.  # noqa: E501

        :return: The all_symbols of this Filing.  # noqa: E501
        :rtype: list[str]
        """
        return self._all_symbols

    @all_symbols.setter
    def all_symbols(self, all_symbols):
        """Sets the all_symbols of this Filing.

        The stock exchange symbols of all filing entities associated with the returned filing.  # noqa: E501

        :param all_symbols: The all_symbols of this Filing.  # noqa: E501
        :type: list[str]
        """

        self._all_symbols = all_symbols

    @property
    def documents(self):
        """Gets the documents of this Filing.  # noqa: E501


        :return: The documents of this Filing.  # noqa: E501
        :rtype: DocumentInfo
        """
        return self._documents

    @documents.setter
    def documents(self, documents):
        """Sets the documents of this Filing.


        :param documents: The documents of this Filing.  # noqa: E501
        :type: DocumentInfo
        """
        if documents is None:
            raise ValueError(
                "Invalid value for `documents`, must not be `None`"
            )  # noqa: E501

        self._documents = documents

    @property
    def edgar_time(self):
        """Gets the edgar_time of this Filing.  # noqa: E501

        The time the EDGAR system recieved the filing.  # noqa: E501

        :return: The edgar_time of this Filing.  # noqa: E501
        :rtype: datetime
        """
        return self._edgar_time

    @edgar_time.setter
    def edgar_time(self, edgar_time):
        """Sets the edgar_time of this Filing.

        The time the EDGAR system recieved the filing.  # noqa: E501

        :param edgar_time: The edgar_time of this Filing.  # noqa: E501
        :type: datetime
        """
        if edgar_time is None:
            raise ValueError(
                "Invalid value for `edgar_time`, must not be `None`"
            )  # noqa: E501

        self._edgar_time = edgar_time

    @property
    def edgar_url(self):
        """Gets the edgar_url of this Filing.  # noqa: E501

        The link to the filings's documents index page on the EDGAR site.  # noqa: E501

        :return: The edgar_url of this Filing.  # noqa: E501
        :rtype: str
        """
        return self._edgar_url

    @edgar_url.setter
    def edgar_url(self, edgar_url):
        """Sets the edgar_url of this Filing.

        The link to the filings's documents index page on the EDGAR site.  # noqa: E501

        :param edgar_url: The edgar_url of this Filing.  # noqa: E501
        :type: str
        """
        if edgar_url is None:
            raise ValueError(
                "Invalid value for `edgar_url`, must not be `None`"
            )  # noqa: E501

        self._edgar_url = edgar_url

    @property
    def filer(self):
        """Gets the filer of this Filing.  # noqa: E501

        The name of the filing entity of the returned filing.  # noqa: E501

        :return: The filer of this Filing.  # noqa: E501
        :rtype: str
        """
        return self._filer

    @filer.setter
    def filer(self, filer):
        """Sets the filer of this Filing.

        The name of the filing entity of the returned filing.  # noqa: E501

        :param filer: The filer of this Filing.  # noqa: E501
        :type: str
        """
        if filer is None:
            raise ValueError(
                "Invalid value for `filer`, must not be `None`"
            )  # noqa: E501

        self._filer = filer

    @property
    def filer_relation(self):
        """Gets the filer_relation of this Filing.  # noqa: E501

        The relation the filing entity has with the filing. Can be any of Reporting, Filer, Issuer, Filed By, Subject, etc.  # noqa: E501

        :return: The filer_relation of this Filing.  # noqa: E501
        :rtype: str
        """
        return self._filer_relation

    @filer_relation.setter
    def filer_relation(self, filer_relation):
        """Sets the filer_relation of this Filing.

        The relation the filing entity has with the filing. Can be any of Reporting, Filer, Issuer, Filed By, Subject, etc.  # noqa: E501

        :param filer_relation: The filer_relation of this Filing.  # noqa: E501
        :type: str
        """
        if filer_relation is None:
            raise ValueError(
                "Invalid value for `filer_relation`, must not be `None`"
            )  # noqa: E501

        self._filer_relation = filer_relation

    @property
    def form_type(self):
        """Gets the form_type of this Filing.  # noqa: E501

        The form type returned filing.  # noqa: E501

        :return: The form_type of this Filing.  # noqa: E501
        :rtype: str
        """
        return self._form_type

    @form_type.setter
    def form_type(self, form_type):
        """Sets the form_type of this Filing.

        The form type returned filing.  # noqa: E501

        :param form_type: The form_type of this Filing.  # noqa: E501
        :type: str
        """
        if form_type is None:
            raise ValueError(
                "Invalid value for `form_type`, must not be `None`"
            )  # noqa: E501

        self._form_type = form_type

    @property
    def id(self):
        """Gets the id of this Filing.  # noqa: E501

        The id of the returned filing, assigned by the filingsdb system.  # noqa: E501

        :return: The id of this Filing.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Filing.

        The id of the returned filing, assigned by the filingsdb system.  # noqa: E501

        :param id: The id of this Filing.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError(
                "Invalid value for `id`, must not be `None`"
            )  # noqa: E501

        self._id = id

    @property
    def primary_cik(self):
        """Gets the primary_cik of this Filing.  # noqa: E501

        The CIK (Central Index Key) of the filing entity of the returned filing.  # noqa: E501

        :return: The primary_cik of this Filing.  # noqa: E501
        :rtype: str
        """
        return self._primary_cik

    @primary_cik.setter
    def primary_cik(self, primary_cik):
        """Sets the primary_cik of this Filing.

        The CIK (Central Index Key) of the filing entity of the returned filing.  # noqa: E501

        :param primary_cik: The primary_cik of this Filing.  # noqa: E501
        :type: str
        """
        if primary_cik is None:
            raise ValueError(
                "Invalid value for `primary_cik`, must not be `None`"
            )  # noqa: E501

        self._primary_cik = primary_cik

    @property
    def primary_symbol(self):
        """Gets the primary_symbol of this Filing.  # noqa: E501

        The stock exchange symbol of the filing entity of the returned filing.  # noqa: E501

        :return: The primary_symbol of this Filing.  # noqa: E501
        :rtype: str
        """
        return self._primary_symbol

    @primary_symbol.setter
    def primary_symbol(self, primary_symbol):
        """Sets the primary_symbol of this Filing.

        The stock exchange symbol of the filing entity of the returned filing.  # noqa: E501

        :param primary_symbol: The primary_symbol of this Filing.  # noqa: E501
        :type: str
        """

        self._primary_symbol = primary_symbol

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
        # if issubclass(Filing, dict):
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
        if not isinstance(other, Filing):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
