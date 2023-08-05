# coding=utf8

"""

 dhunter

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/dhunter

"""

from abc import abstractmethod
from collections import OrderedDict

from .const import Const


class HashBase(object):

    # @property
    # def data_type_filed_name(self) -> str:
    #     return '_type'

    @property
    @abstractmethod
    def data_type(self) -> str:
        raise NotImplementedError

        # return self.DATA_KEY

    # @property
    # def data_version_field_name(self) -> str:
    #     return '_version'

    @property
    @abstractmethod
    def data_version(self) -> int:
        raise NotImplementedError

        # return self.DATA_VERSION

    # @abstractmethod
    # def _get_json_export_attrs(self) -> List[str]:
    #     """Returns list of class attribute names we want to export in JSON representation.
    #     """
    #     raise NotImplementedError

    def _get_base_attrs(self) -> OrderedDict:
        return OrderedDict([
            (Const.FIELD_TYPE, self.data_type),
            (Const.FIELD_VERSION, self.data_version),
        ])

    @abstractmethod
    def to_json(self) -> str:
        """Converts object data into JSON string.
        """
        raise NotImplementedError

    def json_data_valid(self, json_dict: dict) -> bool:
        """Checks if given dict structure based on loaded JSON data matches requirements and is dump of our class
        """
        result = False

        data_type = json_dict.get(Const.FIELD_TYPE)
        version = json_dict.get(Const.FIELD_VERSION)
        if data_type is not None and version is not None:
            result = data_type == self.data_type and version <= self.data_version

        return result
