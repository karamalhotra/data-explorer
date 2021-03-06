# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from data_explorer.models.base_model_ import Model
from data_explorer import util


class FacetValue(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, name=None, count=None):  # noqa: E501
        """FacetValue - a model defined in Swagger

        :param name: The name of this FacetValue.  # noqa: E501
        :type name: str
        :param count: The count of this FacetValue.  # noqa: E501
        :type count: int
        """
        self.swagger_types = {'name': str, 'count': int}

        self.attribute_map = {'name': 'name', 'count': 'count'}

        self._name = name
        self._count = count

    @classmethod
    def from_dict(cls, dikt):
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The FacetValue of this FacetValue.  # noqa: E501
        :rtype: FacetValue
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self):
        """Gets the name of this FacetValue.

        Facet value name, for example, \"Male\".  # noqa: E501

        :return: The name of this FacetValue.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this FacetValue.

        Facet value name, for example, \"Male\".  # noqa: E501

        :param name: The name of this FacetValue.
        :type name: str
        """

        self._name = name

    @property
    def count(self):
        """Gets the count of this FacetValue.

        Facet value count.  # noqa: E501

        :return: The count of this FacetValue.
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this FacetValue.

        Facet value count.  # noqa: E501

        :param count: The count of this FacetValue.
        :type count: int
        """

        self._count = count
