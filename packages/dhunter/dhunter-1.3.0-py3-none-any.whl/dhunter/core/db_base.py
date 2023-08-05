# coding=utf8

"""

 dhunter

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/dhunter

"""

import sqlite3
import typing
from abc import abstractmethod


class DbBase(object):

    def __init__(self, db_file_name: str):
        self.__db = None
        self.__db_file_name = db_file_name

    def __del__(self) -> None:
        self.__db_disconnect()

    # ------------------------------------------------------------------------------------------------------------

    def __db_connect(self):
        if self.db is None:
            self.db = sqlite3.connect(self.__db_file_name)
            # self.db.isolation_level = 'EXCLUSIVE'
            # self.db.execute('BEGIN EXCLUSIVE')
            self.db.row_factory = sqlite3.Row

    def __db_disconnect(self) -> None:
        if self.__db is not None:
            self.__db.commit()

            self.__db.close()
            self.__db = None

    # ------------------------------------------------------------------------------------------------------------

    # @property
    # def db(self) -> sqlite3.Connection:
    #     return self.__db
    #
    # @db.setter
    # def db(self, val: sqlite3.Connection or None) -> None:
    #     self.__db = val

    @abstractmethod
    def create_tables(self) -> None:
        raise NotImplementedError

    def __create_tables(self, queries: typing.List[str]) -> None:
        self.__db_connect()
        _ = [self.__db.cursor().execute(query) for query in queries]

    # ------------------------------------------------------------------------------------------------------------

    def insert(self, item):
        raise NotImplementedError

    def replace(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError
