# coding: utf-8

import pprint
import re  # noqa: F401

import six


class Document(object):

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    swagger_types = {
        "body": "str",
        "description": "str",
        "doc_type": "str",
        "edgar_url": "str",
        "filing_id": "str",
        "id": "str",
        "seq": "int",
        "size_estimate": "str",
    }

    attribute_map = {
        "body": "body",
        "description": "description",
        "doc_type": "docType",
        "edgar_url": "edgarURL",
        "filing_id": "filingID",
        "id": "id",
        "seq": "seq",
        "size_estimate": "sizeEstimate",
    }

    def __init__(
        self,
        body=None,
        description=None,
        doc_type=None,
        edgar_url=None,
        filing_id=None,
        id=None,
        seq=None,
        size_estimate=None,
    ):  # noqa: E501
        """Document - a single document belonging to a filing"""  # noqa: E501

        self._body = None
        self._description = None
        self._doc_type = None
        self._edgar_url = None
        self._filing_id = None
        self._id = None
        self._seq = None
        self._size_estimate = None
        self.discriminator = None

        self.body = body
        self.description = description
        self.doc_type = doc_type
        self.edgar_url = edgar_url
        self.filing_id = filing_id
        self.id = id
        self.seq = seq
        self.size_estimate = size_estimate

    @property
    def body(self):
        """Gets the body of this Document.  # noqa: E501

        The contents of the document.  # noqa: E501

        :return: The body of this Document.  # noqa: E501
        :rtype: str
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this Document.

        The contents of the document.  # noqa: E501

        :param body: The body of this Document.  # noqa: E501
        :type: str
        """
        if body is None:
            raise ValueError(
                "Invalid value for `body`, must not be `None`"
            )  # noqa: E501

        self._body = body

    @property
    def description(self):
        """Gets the description of this Document.  # noqa: E501

        A brief description of the document.  # noqa: E501

        :return: The description of this Document.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Document.

        A brief description of the document.  # noqa: E501

        :param description: The description of this Document.  # noqa: E501
        :type: str
        """
        if description is None:
            raise ValueError(
                "Invalid value for `description`, must not be `None`"
            )  # noqa: E501

        self._description = description

    @property
    def doc_type(self):
        """Gets the doc_type of this Document.  # noqa: E501

        A shortcode specifying the document type.  # noqa: E501

        :return: The doc_type of this Document.  # noqa: E501
        :rtype: str
        """
        return self._doc_type

    @doc_type.setter
    def doc_type(self, doc_type):
        """Sets the doc_type of this Document.

        A shortcode specifying the document type.  # noqa: E501

        :param doc_type: The doc_type of this Document.  # noqa: E501
        :type: str
        """
        if doc_type is None:
            raise ValueError(
                "Invalid value for `doc_type`, must not be `None`"
            )  # noqa: E501

        self._doc_type = doc_type

    @property
    def edgar_url(self):
        """Gets the edgar_url of this Document.  # noqa: E501

        The link to the document's contents on the EDGAR site.  # noqa: E501

        :return: The edgar_url of this Document.  # noqa: E501
        :rtype: str
        """
        return self._edgar_url

    @edgar_url.setter
    def edgar_url(self, edgar_url):
        """Sets the edgar_url of this Document.

        The link to the document's contents on the EDGAR site.  # noqa: E501

        :param edgar_url: The edgar_url of this Document.  # noqa: E501
        :type: str
        """
        if edgar_url is None:
            raise ValueError(
                "Invalid value for `edgar_url`, must not be `None`"
            )  # noqa: E501

        self._edgar_url = edgar_url

    @property
    def filing_id(self):
        """Gets the filing_id of this Document.  # noqa: E501

        The id of the filing that the document belongs to.  # noqa: E501

        :return: The filing_id of this Document.  # noqa: E501
        :rtype: str
        """
        return self._filing_id

    @filing_id.setter
    def filing_id(self, filing_id):
        """Sets the filing_id of this Document.

        The id of the filing that the document belongs to.  # noqa: E501

        :param filing_id: The filing_id of this Document.  # noqa: E501
        :type: str
        """
        if filing_id is None:
            raise ValueError(
                "Invalid value for `filing_id`, must not be `None`"
            )  # noqa: E501

        self._filing_id = filing_id

    @property
    def id(self):
        """Gets the id of this Document.  # noqa: E501

        The unique ID assigned to a document by the filingsdb system.  # noqa: E501

        :return: The id of this Document.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Document.

        The unique ID assigned to a document by the filingsdb system.  # noqa: E501

        :param id: The id of this Document.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError(
                "Invalid value for `id`, must not be `None`"
            )  # noqa: E501

        self._id = id

    @property
    def seq(self):
        """Gets the seq of this Document.  # noqa: E501

        The sequence of the document indicating its position within a filings' document set.  # noqa: E501

        :return: The seq of this Document.  # noqa: E501
        :rtype: int
        """
        return self._seq

    @seq.setter
    def seq(self, seq):
        """Sets the seq of this Document.

        The sequence of the document indicating its position within a filings' document set.  # noqa: E501

        :param seq: The seq of this Document.  # noqa: E501
        :type: int
        """
        if seq is None:
            raise ValueError(
                "Invalid value for `seq`, must not be `None`"
            )  # noqa: E501

        self._seq = seq

    @property
    def size_estimate(self):
        """Gets the size_estimate of this Document.  # noqa: E501

        The size estimate of the document contents.  # noqa: E501

        :return: The size_estimate of this Document.  # noqa: E501
        :rtype: str
        """
        return self._size_estimate

    @size_estimate.setter
    def size_estimate(self, size_estimate):
        """Sets the size_estimate of this Document.

        The size estimate of the document contents.  # noqa: E501

        :param size_estimate: The size_estimate of this Document.  # noqa: E501
        :type: str
        """
        if size_estimate is None:
            raise ValueError(
                "Invalid value for `size_estimate`, must not be `None`"
            )  # noqa: E501

        self._size_estimate = size_estimate

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
        # if issubclass(Document, dict):
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
        if not isinstance(other, Document):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
